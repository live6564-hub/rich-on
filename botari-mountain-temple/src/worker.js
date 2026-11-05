// 🎒 보따리 v1 — 산속 절 함께 걷기 서버
// Cloudflare Workers + Durable Objects (무료 요금제에서 되는 SQLite 저장 방식)
// - public/index.html 은 Workers 정적 파일 기능(assets)으로 같은 주소에서 내보낸다
// - /ws 로 들어오는 WebSocket 만 이 코드가 받는다
// - WebSocket Hibernation(잠자기) 사용: 아무도 말하지 않을 때는 서버가 잠들어서 무료 한도를 아낀다

import { DurableObject } from "cloudflare:workers";

const MAX_PEOPLE = 20;          // 한 방 인원 (public/index.html 의 CONFIG.room.maxPeople 과 같게)
const MAX_MSG_PER_SEC = 8;      // 이보다 자주 보내면 무시 (화면은 1초에 5번만 보냄)

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/ws") {
      if (request.headers.get("Upgrade") !== "websocket") {
        return new Response("WebSocket 으로만 들어올 수 있어요", { status: 426 });
      }
      const room = (url.searchParams.get("room") || "main").slice(0, 32);
      const stub = env.ROOM.get(env.ROOM.idFromName(room));
      return stub.fetch(request);
    }
    // 그 밖의 주소는 정적 파일(public/)이 처리한다. 여기까지 오면 없는 주소.
    return new Response("Not found", { status: 404 });
  },
};

export class Room extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env);
    // 'ping' 에는 서버를 깨우지 않고 자동으로 'pong' 답장 (무료 한도 절약)
    this.ctx.setWebSocketAutoResponse(new WebSocketRequestResponsePair("ping", "pong"));
  }

  async fetch(request) {
    const url = new URL(request.url);
    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);

    // 방이 꽉 찼으면 안내만 보내고 닫는다
    if (this.ctx.getWebSockets().length >= MAX_PEOPLE) {
      server.accept();
      server.send(JSON.stringify({ t: "full", max: MAX_PEOPLE }));
      server.close(4000, "full");
      return new Response(null, { status: 101, webSocket: client });
    }

    const name = cleanName(url.searchParams.get("name"));
    const id = crypto.randomUUID().slice(0, 8);
    const me = { id, name, x: 0, y: 0, z: 6, ry: Math.PI, act: 0, lastT: 0, count: 0 };

    // 지금 있는 사람 목록 (잠에서 깨도 attachment 에 저장된 위치로 복원됨)
    const peers = this.ctx.getWebSockets().map((ws) => publicInfo(ws.deserializeAttachment())).filter(Boolean);

    this.ctx.acceptWebSocket(server);
    server.serializeAttachment(me);
    server.send(JSON.stringify({ t: "welcome", id, peers }));
    this.broadcast({ t: "join", ...publicInfo(me) }, server);

    return new Response(null, { status: 101, webSocket: client });
  }

  async webSocketMessage(ws, message) {
    if (typeof message !== "string" || message.length > 300) return;
    let msg;
    try { msg = JSON.parse(message); } catch { return; }
    if (msg.t !== "pos") return;

    const me = ws.deserializeAttachment();
    if (!me) return;

    // 너무 자주 보내면 무시
    const now = Date.now();
    if (now - me.lastT > 1000) { me.lastT = now; me.count = 0; }
    if (++me.count > MAX_MSG_PER_SEC) { ws.serializeAttachment(me); return; }

    me.x = num(msg.x, -40, 40);
    me.y = num(msg.y, -1, 5);
    me.z = num(msg.z, -40, 40);
    me.ry = num(msg.ry, -1000, 1000);
    me.act = Math.max(0, Math.min(3, Math.round(Number(msg.act) || 0)));   // 0 걷기 · 1 합장 · 2 앉기 · 3 절하기
    me.tap = Math.max(0, Math.min(1e6, Math.round(Number(msg.tap) || 0)));  // 목탁 두드린 횟수
    ws.serializeAttachment(me);

    this.broadcast({ t: "pos", ...publicInfo(me) }, ws);
  }

  async webSocketClose(ws, code, reason) {
    this.leave(ws);
    try { ws.close(code, reason); } catch {}
  }

  async webSocketError(ws) {
    this.leave(ws);
  }

  leave(ws) {
    const me = ws.deserializeAttachment();
    if (me) this.broadcast({ t: "leave", id: me.id }, ws);
  }

  broadcast(obj, except) {
    const text = JSON.stringify(obj);
    for (const ws of this.ctx.getWebSockets()) {
      if (ws === except) continue;
      try { ws.send(text); } catch {}
    }
  }
}

function publicInfo(a) {
  if (!a) return null;
  return { id: a.id, name: a.name, x: a.x, y: a.y, z: a.z, ry: a.ry, act: a.act, tap: a.tap || 0 };
}
function num(v, lo, hi) {
  const n = Number(v);
  if (!Number.isFinite(n)) return 0;
  return Math.max(lo, Math.min(hi, Math.round(n * 100) / 100));
}
function cleanName(v) {
  const s = String(v || "").replace(/[<>&"'`]/g, "").trim().slice(0, 10);
  return s || "손님";
}
