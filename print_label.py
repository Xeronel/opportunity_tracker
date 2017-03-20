import sys
from subprocess import call
from os import devnull
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont


# Register fonts
fonts = ['OpenSans-Bold', 'OpenSans-Regular']
for font in fonts:
    f = TTFont(font, 'fonts/' + font + '.ttf')
    registerFont(f)

lblSize = (216, 72)
lblPath = '/tmp/label.pdf'
bold = 'OpenSans-Bold'
regular = 'OpenSans-Regular'
top = 56
left = 4
middle = 32
bottom = 6


def print_label(top_left, center, bottom_left, copies):
    c = canvas.Canvas(lblPath, pagesize=lblSize)

    # Draw top left
    c.setFont(bold, 16)
    c.drawString(left, top, str(top_left).upper())

    # Draw left center
    c.setFont(regular, 12)
    c.drawString(left, middle, str(center).upper())

    # Draw bottom
    c.setFont(regular, 12)
    c.drawString(left, bottom, str(bottom_left).upper())

    # Finalize page and save file
    c.showPage()
    c.save()

    # Print label
    call(['/usr/bin/lp', lblPath, '-n', copies],
         stdout=open(devnull, 'w'),
         close_fds=True)


if __name__ == '__main__':
    print_label(*sys.argv[1:])
