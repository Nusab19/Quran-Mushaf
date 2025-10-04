import os
import time
import pypdfium2 as pdfium


def goToRoot():
    cwd = os.getcwd()
    if cwd.endswith("src"):
        os.chdir("..")  # go to project root

    print("Current working directory:", os.getcwd())


def makeDir(path):
    os.makedirs(path, exist_ok=True)


def saveImages(quality="high"):
    imageDir = f"dist/{quality}/"
    pdfPath = "data/almadinah-kabir-azraq.pdf"
    pdf = pdfium.PdfDocument(pdfPath)
    totalPages = len(pdf)
    scales = {
        "very-low": 1,
        "low": 1.5,
        "medium": 2,
        "high": 3,
        "very-high": 4,
    }
    makeDir(imageDir)

    startTime = time.time()

    print(f"Total pages in PDF: {totalPages}")

    for index, page in enumerate(pdf, start=1):
        bitmap = page.render(
            # `1` means 72 dpi. We're using 3 for 216 dpi. You can use other scales too.
            # Higher scale means better quality but larger image. But after a certain point, you'll see no difference in quality.
            # But the size will keep increasing. So better not use more than `5`.
            scale=scales[quality],  # default is 3
            rotation=0,
        )
        image = bitmap.to_pil()
        image.save(
            os.path.join(imageDir, f"{index:03}.jpg"),
            format="JPEG",  # saving as JPEG instead of PNG reduces the size a lot.
            quality=100,
            optimize=True,  # optimizing it reduces the size a bit. but doesn't make much difference in quality.
            progressive=True,  # you can disable this if you don't need "progressive loading" feature.
        )
        bitmap.close()
        print(f"Saved {index + 1:03}/{totalPages}\r", end="", flush=True)

    print(f"\nDone saving {totalPages} images.")
    print(f"Time taken: {time.time() - startTime:.2f} seconds.")


if __name__ == "__main__":
    goToRoot()

    # You can change the quality to "very-low", "low", "medium", "high", or "very-high"
    # You don't need to run all qualities. Just run the one you need.
    
    saveImages("low")
    # saveImages("medium")
    # saveImages("high")
