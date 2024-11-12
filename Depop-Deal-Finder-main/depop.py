"""
Application to scrape data from depop and filter prices.
Team members: Ibrahim Wifak, Zijin Wang, Marcelo Soriano, Madina Diane
Date: 4_9_2024

Instructions: Enter Category (mens or womens), MAX price, and size (optional)
"""
from bs4 import BeautifulSoup #used for web scraping
from selenium.webdriver import Chrome #used for accessing the content from a javascript rendered site
from selenium.webdriver import ChromeOptions #used for headless access
from argparse import ArgumentParser #used to run the script with a command line
from datetime import datetime #imports the date and time libraries for the txt
import sys

class DepopScraper:
    """Class that represents a Depop Scraper

    Attributes:
        url (str): the link based on the category chosen
        price (float): the max price of the items
        size (str): the size of the clothes
    """
    def __init__(self, url, price, size=None):
        self.url = url
        self.price = price
        self.size = size

    def get_page_source(self):
        """ Function to get page source
        
        Returns:
            page_source (page_source): the page "content"
        """
        option = ChromeOptions()
        #allows for the webrower to open in icognito
        option.add_argument("--incognito")

        driver = Chrome(options=option)

        driver.get(self.url)
        page_source = driver.page_source
        driver.quit()

        return page_source

    def get_data(self, page_source):
        """ Function to get the data from the html content

        Parameters:
            html (str): html content
        
        Returns:
            data_list (list): the extracted data
        """
        soup = BeautifulSoup(page_source, 'html.parser')

        #Finds all list items
        products = soup.find_all('li', class_="styles__ProductCardContainer-sc-4aad5806-7 kDwiaz")

        #declares an empty list
        scraped_products = []

        #loops through the products (all li/list elements)
        for p in products:
            link = p.find('a', class_='styles__ProductCard-sc-4aad5806-4 ffvUlI')
            if link:
                href = link.get('href')

            #If the sale price is found then that will be the price value
            price_sale = p.find('p', class_='sc-eDnWTT Price-styles__DiscountPrice-sc-f7c1dfcc-1 fRxqiS KMEBr')
            if price_sale is not None:
                price_t = price_sale.text.strip().replace('$','')
                if price_t:
                    price = float(price_t)
            else:
                #If the sale isnt found then the regular price will be scraped and set
                price_e = p.find('p', class_='sc-eDnWTT Price-styles__FullPrice-sc-f7c1dfcc-0 fRxqiS hmFDou')
                if price_e is not None:
                    price_t = price_e.text.strip().replace('$','')
                    if price_t:
                        price = float(price_t)

            size = None
            if p.find('p', class_='sc-eDnWTT styles__StyledSizeText-sc-4aad5806-12 kcKICQ cuCvzt'):
                size = p.find('p', class_='sc-eDnWTT styles__StyledSizeText-sc-4aad5806-12 kcKICQ cuCvzt').text.strip()

            #Assigning keys and values for dict
            product_info = {
                'link': "depop.com" + href,
                'price': price,
                'size': size
            }

            scraped_products.append(product_info)
        
        return scraped_products

    def scrape(self):
        """Method that scrapes the product cards

        Returns:
            list (list): list after using the get_data() method
        """
        page_source = self.get_page_source()

        return self.get_data(page_source)
    
def filter_data_price(products, price):
    """Function to filter the data by price
    
    Parameters:
        products (dict): the list of items scraped
        price (float): the price we want to filter by
    
    Returns:
        price_list (list): a list filtered by price
    """
    #empty list for the price
    filtered_products = []

    for f in products:
        #if the price is less than or equal to the price then it appends it to a list
        if f['price'] <= price:
            filtered_products.append(f)
    
    return filtered_products

def filter_data_size(products, size):
    """Function to filter the data by size
    
    Parameters:
        products (dict): the list of items scraped
        size (str): the size we want to filter by
    
    Returns:
        filtered_products_S (list): a list filtered by size (if size is applicable)
    """
    #Size is naturally none since it is optional
    if size is None:
        #If the size is none then it returns the list without altering it
        return products
    else:
        #Empty list for the size
        filtered_products_S = []

        #for the products in the products dictionary
        for f in products:
            #If the size is pulled through scraping (size attribute on depop)
            if f['size'] is not None:
                #Checks for the shoe size since it all begins with US
                if f['size'].startswith("US"):
                    shoe_size = f['size'][3:]

                    #If the shoe size = the size we specified.
                    if shoe_size == size:
                        filtered_products_S.append(f)

                #Checks for the pant size in depop since 
                elif f['size'].endswith('"'):
                    pants_size = f['size'][:-1]
                    
                    #If the pant size = the size we specified.
                    if pants_size == size:
                        filtered_products_S.append(f)
                        
                else:
                    #If the size is numerical
                    if f['size'] == size:
                        filtered_products_S.append(f)

        #return the filtered list
        return filtered_products_S

def output_data(products):
    """Function that prints the items after they were filtered
    
    Parameters:
        products (list): the filtered information
    """
    #For product in products we print the entire list of items found
    for p in products:
        print(f"Link: {p['link']}")
        print(f"Price: ${p['price']}")
        print(f"Size: {p['size']}")
        print("-" * 20)
        print()
        
def generate_url(category):
    """Function to generate the url based on the category chosen

    Parameters:
        category (str): the category the user chose

    Returns:
        url (str): the string based on te category
    """
    #the base url since only thing different is the mens or womens at the end
    base = 'https://www.depop.com/category/'

    try:
        #If the category chosen is mens then it sets the link to the mens section
        if category.lower() == 'mens':
            url = base + "mens/"
            return url
        #If the category chosen is womens then it sets the link to the womens section
        elif category.lower() == 'womens':
            url = base + "womens/"
            return url
        else:
            #Raises an error if someone choses anything other than mens or womens
            raise ValueError("Invalid Category. Please enter mens or womens.")
    except ValueError as e:
        print(e)

def write_file(products):
    """Function to write the listings' information to a file

    Parameters:
        products (list): the filtered information
    """
    #Opens/Creates a depop.txt file using the append mode
    with open('depop.txt', 'a') as f:
        #Uses the datetime library to get current time and set the format as instructed
        date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        f.write('Date: ' + date + ' \n')
        #For all products in the products list
        for p in products:
            f.write(f"Link: {p['link']} \n")
            f.write(f"Price: ${p['price']} \n")
            f.write(f"Size: {p['size']} \n")

def parse_args(arglist):
    """ Function to run scripts with command line

    Returns:
        parser.parse_args(arglist): parsed arguments
    """
    parser = ArgumentParser(description='Scrape Depop listings based on category(mens or womens), price, and size.')
    parser.add_argument('category', type=str, help='Enter "mens" or "womens" as a category')
    parser.add_argument('price', type=float, help='Enter the maximum price for items')
    parser.add_argument('--size', type=str, help='Enter your size (e.g. S, M, L, XL)')

    return parser.parse_args(arglist)

def main():
    """Main function to scrape Depop listings based on user inputs.
    """
    args = parse_args(sys.argv[1:])

    category = args.category
    price = args.price
    size = args.size

    #generates the url
    url = generate_url(category)
    #create an instance of the class
    scrapper = DepopScraper(url, price, size)

    scrape_products = scrapper.scrape()
    
    filter_price = filter_data_price(scrape_products, price)
    
    filtered = filter_data_size(filter_price, size)

    output_products = output_data(filtered)

    write_data = write_file(filtered)

if __name__ == "__main__":
    main()