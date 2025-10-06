from rembg import remove
from PIL import Image
import sys
import os

def remove_background(input_path, output_path=None):
    try:
        if not os.path.exists(input_path):
            print(f"Hata: '{input_path}' dosyası bulunamadı!")
            return False
        
        if output_path is None:
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_no_bg.png"
        
        print(f"İşleniyor: {input_path}")
        
        with open(input_path, 'rb') as inp:
            input_data = inp.read()
        
        output_data = remove(input_data)
        
        with open(output_path, 'wb') as out:
            out.write(output_data)
        
        print(f"✓ Başarılı! Kaydedildi: {output_path}")
        return True
        
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        return False

def batch_remove_background(input_folder, output_folder=None):
    if output_folder is None:
        output_folder = f"{input_folder}_no_bg"
    
    os.makedirs(output_folder, exist_ok=True)
    
    extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
    
    files = [f for f in os.listdir(input_folder) 
             if f.lower().endswith(extensions)]
    
    if not files:
        print("Klasörde işlenecek fotoğraf bulunamadı!")
        return
    
    print(f"{len(files)} fotoğraf bulundu. İşleniyor...\n")
    
    success = 0
    for i, filename in enumerate(files, 1):
        input_path = os.path.join(input_folder, filename)
        name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_folder, f"{name}_no_bg.png")
        
        print(f"[{i}/{len(files)}] ", end="")
        if remove_background(input_path, output_path):
            success += 1
        print()
    
    print(f"\nToplam: {len(files)} fotoğraf")
    print(f"Başarılı: {success}")
    print(f"Başarısız: {len(files) - success}")

def main():
    if len(sys.argv) < 2:
        print("Kullanım:")
        print("  Tek fotoğraf: python program.py input.jpg [output.png]")
        print("  Toplu işlem:  python program.py klasor/ [cikis_klasoru/]")
        print("\nÖrnekler:")
        print("  python program.py foto.jpg")
        print("  python program.py foto.jpg sonuc.png")
        print("  python program.py fotolar/")
        print("  python program.py fotolar/ sonuclar/")
        return
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if os.path.isdir(input_path):
        batch_remove_background(input_path, output_path)
    else:
        remove_background(input_path, output_path)

if __name__ == "__main__":
    main()
