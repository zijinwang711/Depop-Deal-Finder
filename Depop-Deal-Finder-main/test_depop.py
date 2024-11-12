import pytest
import depop as d
import unittest

class Test_depop (unittest.TestCase):
    """Class that represents a tester for an application"""
    """ This class contains various test methods to ensure 
    the correct functionality of the depop scraper application"""
    
    def test_generate_url_mens(self):
        """Function to test if mens generates the appropriate url"""
        """ This test checks if the 'generate_url' function returns the correct url
        for the 'mens' category on the Depop website"""
        url = d.generate_url('mens')
        self.assertEqual (url , 'https://www.depop.com/category/mens/')

    def test_generate_url_womens(self):
        """Function to test if womens generates the appropriate url"""
        """ This test checks if the 'generate_url' function returns the correct url
        for the 'womens' category on the Depop website"""
        url = d.generate_url('womens')
        self.assertEqual (url , 'https://www.depop.com/category/womens/')

    def test_filter_data_size(self):
        """Function to test the filtering function for the size"""
        """ This test checks if the 'filter_data_size' function correctly filters 
        the product data based on the specified size"""
        sample_products = [
            {'link': 'depop.com/mens', 'price': 20.0, 'size': 'L'},
            {'link': 'depop.com/womens', 'price': 30.0, 'size': 'L'},
            {'link': 'depop.com/mens', 'price': 25.0, 'size': 'US 10.5'}
        ]

        filtered = d.filter_data_size(sample_products, 'L')
        self.assertEqual (len(filtered) , 2)

        filtered = d.filter_data_size(sample_products, '10.5')
        self.assertEqual (len(filtered) , 1)

        filtered = d.filter_data_size(sample_products, 'XXL')
        self.assertEqual (len(filtered) , 0) 

    def test_filter_data_price(self):
        """Function to test the filtering function for the price"""
        """ This test checks if the 'filter_data_price' function correctly filters 
        the product data based on the specified price"""
        sample_products = [
            {'link': 'depop.com/mens', 'price': 20.0, 'size': 'L'},
            {'link': 'depop.com/womens', 'price': 30.0, 'size': 'M'},
            {'link': 'depop.com/mens', 'price': 25.0, 'size': '10.5'}
        ]

        filtered = d.filter_data_price(sample_products, 20)
        self.assertEqual (len(filtered) , 1)

        for f in filtered:      
            self.assertEqual (f['price'] , 20)
        
        
    def test_get_data(self):
        """Checks that get_data extracts the correct data from HTML."""
        """ This test checks if the 'get_data' function correctly extracts 
        product details (link, price and size) from the provided HTML content"""
        # Mock HTML with product details.
        html_content = '''
        <html>
        <body>
            <li class="styles__ProductCardContainer-sc-4aad5806-7 kDwiaz">
                <a class="styles__ProductCard-sc-4aad5806-4 ffvUlI" href="/product1">Product 1</a>
                <p class="sc-eDnWTT Price-styles__DiscountPrice-sc-f7c1dfcc-1 fRxqiS KMEBr">$10.00</p>
                <p class="sc-eDnWTT styles__StyledSizeText-sc-4aad5806-12 kcKICQ cuCvzt">M</p>
            </li>
            <li class="styles__ProductCardContainer-sc-4aad5806-7 kDwiaz">
                <a class="styles__ProductCard-sc-4aad5806-4 ffvUlI" href="/product2">Product 2</a>
                <p class="sc-eDnWTT Price-styles__FullPrice-sc-f7c1dfcc-0 fRxqiS hmFDou">$20.00</p>
                <p class="sc-eDnWTT styles__StyledSizeText-sc-4aad5806-12 kcKICQ cuCvzt">L</p>
            </li>
        </body>
        </html>
        '''

        # Define what the correct output should be.
        expected_data = [
            {'link': 'depop.com/product1', 'price': 10.0, 'size': 'M'},
            {'link': 'depop.com/product2', 'price': 20.0, 'size': 'L'}
        ]

        # Create a scraper instance and test data extraction.
        scraper = d.DepopScraper("http://example.com", 100.0, "M")
        result = scraper.get_data(html_content)

        # Ensure the data matches expected output.
        self.assertEqual(result, expected_data)