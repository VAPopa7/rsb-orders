from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
import time

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    open_robot_order_website()
    download_csv()
    orders = get_orders()
    for order in orders:
        constitutional_rights()
        fill_the_form(order)
        pdf_file = store_receipt_as_pdf(order)
        screenshot = screenshot_robot(order)
        embed_screenshot_to_receipt(screenshot, pdf_file)
    #time.sleep(300)

def open_robot_order_website():
    """Opens the robot order website"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def download_csv():
    """Downloads the .csv file from website"""
    http = HTTP()
    http.download("https://robotsparebinindustries.com/orders.csv", overwrite=True)

def get_orders():
    """Converts .csv file to table"""
    table = Tables()
    orders = table.read_table_from_csv("orders.csv", header=True)
    return orders

def fill_the_form(order):
    "Fills in the order data on the website"
    page = browser.page()
    page.select_option("#head", order['Head'])
    page.click(f"//input[@type='radio' and @name='body' and @id='id-body-{order['Body']}' and @value='{order['Body']}']")
    page.fill("//input[@placeholder='Enter the part number for the legs']", order['Legs'])
    page.fill("#address", order['Address'])
    time.sleep(5)
    page.click("//button[@id='order' and @type='submit' and contains(@class, 'btn btn-primary')]")
    i = 1
    while i == 1:
        if page.is_visible("//div[@class='alert alert-danger' and @role='alert']"):
            page.click("//button[@id='order' and @type='submit' and contains(@class, 'btn btn-primary')]")
        else:
            i = 2


def constitutional_rights():
    "Clicks away the pop-up"
    page = browser.page()
    page.click("//button[@type='button' and contains(@class, 'btn btn-dark') and text()='OK']")

def store_receipt_as_pdf(order):
    page = browser.page()
    receipt_html = page.locator("#receipt").inner_html()
    pdf = PDF()
    order_num = order["Order number"]
    pdf.html_to_pdf(receipt_html, f"output/{order_num}_receipt.pdf")
    pdf_file = f"output/{order_num}_receipt.pdf"
    return pdf_file

def screenshot_robot(order):
    page = browser.page()
    order_num = order["Order number"]
    page.screenshot(path=f"output/{order_num}_screenshot.png")
    screenshot = f"output/{order_num}_screenshot.png"
    return screenshot

def embed_screenshot_to_receipt(screenshot, pdf_file):
    pdf = PDF()
    list_of_files = [
        pdf_file,
        screenshot
    ]
    order = screenshot[7] + "_result"
    pdf.add_files_to_pdf(
        files = list_of_files,
        target_document = f"output/{order}.pdf"
    )
    page = browser.page()
    page.click("//button[@id='order-another' and @type='submit' and contains(@class, 'btn btn-primary') and text()='Order another robot']")