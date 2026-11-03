"""Converts the rendered package PNGs to compact WebP (run after build_package_images.js)."""
import glob, os
from PIL import Image
D = os.path.join(os.path.dirname(__file__), '..', 'wp-content', 'plugins', 'seo-booster-core', 'data', 'images')
for f in glob.glob(os.path.join(D, '*.png')):
    Image.open(f).convert('RGB').resize((960, 720), Image.LANCZOS).save(f[:-4] + '.webp', 'WEBP', quality=80, method=6)
    os.remove(f)
print(len(glob.glob(os.path.join(D, '*.webp'))), 'webp files')
