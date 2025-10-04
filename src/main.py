import os
import time
import pypdfium2 as pdfium
from multiprocessing import Pool, cpu_count


def goToRoot():
    cwd = os.getcwd()
    if cwd.endswith("src"):
        os.chdir("..")  # go to project root

    colorPrint("Current working directory:", os.getcwd())


def makeDir(path):
    os.makedirs(path, exist_ok=True)


def colorPrint(*args, color="blue", **kwargs):
    if not args:
        print(**{k: v for k, v in kwargs.items() if k != "color"})
        return

    # Extract sep from kwargs (default ' ')
    sep = kwargs.get("sep", " ")
    text = sep.join(map(str, args))

    if color:
        colorCodes = {
            "blue": "\033[34m",
            "purple": "\033[35m",
            "green": "\033[32m",
            "red": "\033[31m",
            "orange": "\033[33m",
        }
        prefix = colorCodes.get(color, "")
        suffix = "\033[0m" if prefix else ""
        text = f"{prefix}{text}{suffix}"

    kw = {k: v for k, v in kwargs.items() if k != "color"}
    print(text, **kw)


def renderPage(args):
    pdfPath, index, scale, imageDir = args
    pdf = pdfium.PdfDocument(pdfPath)
    page = pdf[index - 1]
    bitmap = page.render(
        # `1` means 72 dpi. We're using 3 for 216 dpi. You can use other scales too.
        # Higher scale means better quality but larger image. But after a certain point, you'll see no difference in quality.
        # But the size will keep increasing. So better not use more than `5`.
        scale=scale,  # default is 3
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
    pdf.close()


def saveImages(quality="high"):
    imageDir = f"dist/{quality}/"
    pdfPath = "data/almadinah-kabir-azraq.pdf"
    pdf = pdfium.PdfDocument(pdfPath)
    totalPages = len(pdf)
    pdf.close()

    scales = {
        "very-low": 1,
        "low": 1.5,
        "medium": 2,
        "high": 3,
        "very-high": 4,
    }
    scale = scales[quality]
    makeDir(imageDir)

    startTime = time.time()

    colorPrint(f"Total pages in PDF: {totalPages}", color="purple")

    args = [(pdfPath, index, scale, imageDir) for index in range(1, totalPages + 1)]

    with Pool(processes=cpu_count()) as pool:
        for i, _ in enumerate(pool.imap(renderPage, args), 1):
            colorPrint(f"Saved {i:03}/{totalPages}\r", end="", flush=True, color="green")

    colorPrint(f"\nDone saving {totalPages} images", color="orange")
    colorPrint(f"Quality: {quality}", color="orange")
    colorPrint(f"Time taken: {time.time() - startTime:.2f} seconds\n", color="orange")


if __name__ == "__main__":
    goToRoot()

    # You can change the quality to "very-low", "low", "medium", "high", or "very-high"
    # You don't need to run all qualities. Just run the one you need.
    saveImages("low")
    saveImages("medium")
    saveImages("high")
