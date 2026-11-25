#!/usr/bin/env python3
"""작은 상품 사진을 무료로 선명하게 키운다 (크레딧 0, 이 컴퓨터 안에서만 처리).

1순위: OpenCV EDSR ×4 공개 모델 (처음 한 번 약 38MB 내려받음, 552px 사진 기준 약 1분)
2순위: 실패하면 Pillow LANCZOS 확대 + 선명 보정
이미 1600px 이상이면 키우지 않고 JPG로만 저장한다.

사용: python3 upscale_photo.py 원본사진 out/vNN/img/product_hd.jpg
필요: pip install "opencv-contrib-python-headless<5" pillow   (2순위는 pillow만)
"""
import sys
import urllib.request
from pathlib import Path

from PIL import Image, ImageFilter

MODEL_URL = "https://raw.githubusercontent.com/Saafke/EDSR_Tensorflow/master/models/EDSR_x4.pb"
MODEL = Path.home() / ".cache" / "detail-page-maker" / "EDSR_x4.pb"
MAX_W = 2400  # 너무 크면 페이지가 무거워진다


def edsr(src: Path):
    import cv2  # noqa: PLC0415
    from cv2 import dnn_superres  # noqa: PLC0415

    if not MODEL.exists() or MODEL.stat().st_size < 1_000_000:
        MODEL.parent.mkdir(parents=True, exist_ok=True)
        print("  모델 내려받는 중 (처음 한 번)…")
        urllib.request.urlretrieve(MODEL_URL, MODEL)
    sr = dnn_superres.DnnSuperResImpl_create()
    sr.readModel(str(MODEL))
    sr.setModel("edsr", 4)
    img = cv2.imread(str(src))
    up = sr.upsample(img)
    blur = cv2.GaussianBlur(up, (0, 0), 1.2)
    up = cv2.addWeighted(up, 1.25, blur, -0.25, 0)
    return Image.fromarray(cv2.cvtColor(up, cv2.COLOR_BGR2RGB))


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    dst.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src).convert("RGB")
    how = "원본 유지"
    if im.width < 1600:
        try:
            im, how = edsr(src), "EDSR ×4 (무료 공개 모델)"
        except Exception as e:  # noqa: BLE001
            print(f"  EDSR 실패 → 기본 확대로 대체: {e}")
            im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS).filter(
                ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
            how = "LANCZOS ×3 + 선명 보정"
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    im.save(dst, quality=92, optimize=True)
    print(f"✅ {dst} · {im.width}×{im.height} · {how}")


if __name__ == "__main__":
    main()
