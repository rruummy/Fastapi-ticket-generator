from io import BytesIO

import qrcode

from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def generate_ticket_pdf(data) -> BytesIO:
    # ---------------------------------------------------------
    # Boarding pass
    # ---------------------------------------------------------

    width = 756
    height = 303

    buffer = BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=(width, height),
    )

    # ---------------------------------------------------------
    # Colors
    # ---------------------------------------------------------

    purple = colors.HexColor("#7B2CBF")
    dark = colors.HexColor("#222222")
    gray = colors.HexColor("#555555")
    light_gray = colors.HexColor("#CCCCCC")

    # ---------------------------------------------------------
    # Data
    # ---------------------------------------------------------

    departure_code = data.departure_code
    arrival_code = data.arrival_code

    departure_city = data.departure_city
    arrival_city = data.arrival_city

    passenger_name = data.passenger_name
    flight_number = data.flight_number
    seat_number = data.seat_number
    airline = data.airline

    # ---------------------------------------------------------
    # Фон
    # ---------------------------------------------------------

    pdf.setFillColor(colors.white)

    pdf.roundRect(
        10,
        10,
        width - 20,
        height - 20,
        15,
        fill=1,
        stroke=0,
    )

    # ---------------------------------------------------------
    # Верхня фіолетова частина
    # ---------------------------------------------------------

    pdf.setFillColor(purple)

    pdf.roundRect(
        10,
        height - 65,
        width - 20,
        55,
        15,
        fill=1,
        stroke=0,
    )

    # Закриваємо нижню частину заокруглення

    pdf.rect(
        10,
        height - 65,
        width - 20,
        20,
        fill=1,
        stroke=0,
    )

    # ---------------------------------------------------------
    # Заголовок
    # ---------------------------------------------------------

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 18)

    pdf.drawString(
        35,
        height - 45,
        "AIRLINE TICKET",
    )

    pdf.drawCentredString(
        width / 2,
        height - 45,
        "BOARDING PASS",
    )

    # ---------------------------------------------------------
    # Вертикальна лінія перед відривною частиною
    # ---------------------------------------------------------

    separator_x = 570

    pdf.setStrokeColor(light_gray)
    pdf.setDash(4, 4)

    pdf.line(
        separator_x,
        20,
        separator_x,
        height - 15,
    )

    pdf.setDash()

    # ---------------------------------------------------------
    # FROM
    # ---------------------------------------------------------

    pdf.setFillColor(gray)
    pdf.setFont("Helvetica-Bold", 9)

    pdf.drawString(
        45,
        215,
        "FROM:",
    )

    pdf.setFillColor(purple)
    pdf.setFont("Helvetica-Bold", 38)

    pdf.drawString(
        45,
        165,
        departure_code,
    )

    pdf.setFillColor(dark)
    pdf.setFont("Helvetica-Bold", 16)

    pdf.drawString(
        45,
        145,
        departure_city.upper(),
    )

    # ---------------------------------------------------------
    # TO
    # ---------------------------------------------------------

    pdf.setFillColor(gray)
    pdf.setFont("Helvetica-Bold", 9)

    pdf.drawString(
        300,
        215,
        "TO:",
    )

    pdf.setFillColor(purple)
    pdf.setFont("Helvetica-Bold", 38)

    pdf.drawString(
        300,
        165,
        arrival_code,
    )

    pdf.setFillColor(dark)
    pdf.setFont("Helvetica-Bold", 16)

    pdf.drawString(
        300,
        145,
        arrival_city.upper(),
    )

    # ---------------------------------------------------------
    # Літак між містами
    # ---------------------------------------------------------

    pdf.setFillColor(purple)
    pdf.setFont("Helvetica-Bold", 28)

    pdf.drawCentredString(
        250,
        170,
        "✈",
    )

    # ---------------------------------------------------------
    # Дата / час
    # ---------------------------------------------------------

    pdf.setFillColor(dark)
    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        45,
        125,
        data.departure_time.strftime("%b %d, %Y"),
    )

    pdf.drawString(
        45,
        110,
        data.departure_time.strftime("%H:%M"),
    )

    pdf.drawString(
        300,
        125,
        data.arrival_time.strftime("%b %d, %Y"),
    )

    pdf.drawString(
        300,
        110,
        data.arrival_time.strftime("%H:%M"),
    )

    # ---------------------------------------------------------
    # Дані пасажира
    # ---------------------------------------------------------

    y_label = 75
    y_value = 55

    columns = [
        (
            "PASSENGER NAME",
            passenger_name,
            45,
        ),
        (
            "FLIGHT",
            flight_number,
            250,
        ),
        (
            "SEAT",
            seat_number,
            345,
        ),
        (
            "AIRLINE",
            airline,
            410,
        ),
    ]

    for label, value, x in columns:

        pdf.setFillColor(gray)
        pdf.setFont("Helvetica-Bold", 7)

        pdf.drawString(
            x,
            y_label,
            label,
        )

        pdf.setFillColor(dark)
        pdf.setFont("Helvetica-Bold", 11)

        pdf.drawString(
            x,
            y_value,
            str(value),
        )

    # ---------------------------------------------------------
    # QR CODE
    # ---------------------------------------------------------

    qr_data = (
        f"ticket:{data.ticket_id};"
        f"flight:{flight_number};"
        f"seat:{seat_number}"
    )

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=6,
        border=2,
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    qr_image = qr.make_image(
        fill_color="black",
        back_color="white",
    )

    qr_buffer = BytesIO()

    qr_image.save(
        qr_buffer,
        format="PNG",
    )

    qr_buffer.seek(0)

    qr_reader = ImageReader(qr_buffer)

    # ---------------------------------------------------------
    # Основний QR
    # ---------------------------------------------------------

    pdf.drawImage(
        qr_reader,
        455,
        110,
        width=90,
        height=90,
        preserveAspectRatio=True,
        anchor="c",
        mask="auto",
    )

    # ---------------------------------------------------------
    # Відривна частина
    # ---------------------------------------------------------

    pdf.setFillColor(gray)
    pdf.setFont("Helvetica-Bold", 7)

    pdf.drawString(
        590,
        215,
        "FROM",
    )

    pdf.drawString(
        590,
        155,
        "TO",
    )

    # ---------------------------------------------------------
    # Коди аеропортів
    # ---------------------------------------------------------

    pdf.setFillColor(purple)
    pdf.setFont("Helvetica-Bold", 24)

    pdf.drawString(
        590,
        180,
        departure_code,
    )

    pdf.drawString(
        590,
        125,
        arrival_code,
    )

    # ---------------------------------------------------------
    # Пасажир
    # ---------------------------------------------------------

    pdf.setFillColor(gray)
    pdf.setFont("Helvetica-Bold", 7)

    pdf.drawString(
        590,
        85,
        "PASSENGER NAME",
    )

    pdf.setFillColor(dark)
    pdf.setFont("Helvetica-Bold", 10)

    # Якщо ім'я довге — трохи зменшуємо шрифт

    passenger_font_size = 10

    if len(passenger_name) > 20:
        passenger_font_size = 8

    pdf.setFont(
        "Helvetica-Bold",
        passenger_font_size,
    )

    pdf.drawString(
        590,
        70,
        passenger_name,
    )

    # ---------------------------------------------------------
    # Seat / Airline
    # ---------------------------------------------------------

    small_data = [
        (
            "SEAT",
            seat_number,
            590,
        ),
        (
            "AIRLINE",
            airline,
            650,
        ),
    ]

    for label, value, x in small_data:

        pdf.setFillColor(gray)
        pdf.setFont("Helvetica-Bold", 6)

        pdf.drawString(
            x,
            45,
            label,
        )

        pdf.setFillColor(dark)

        # Для airline використовуємо менший шрифт,
        # якщо назва довга

        value_font_size = 9

        if label == "AIRLINE" and len(str(value)) > 10:
            value_font_size = 7

        pdf.setFont(
            "Helvetica-Bold",
            value_font_size,
        )

        pdf.drawString(
            x,
            30,
            str(value),
        )

    # ---------------------------------------------------------
    # QR на відривній частині
    # ---------------------------------------------------------

    pdf.drawImage(
        qr_reader,
        700,
        25,
        width=45,
        height=45,
        preserveAspectRatio=True,
        anchor="c",
        mask="auto",
    )

    # ---------------------------------------------------------
    # Завершення PDF
    # ---------------------------------------------------------

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    return buffer