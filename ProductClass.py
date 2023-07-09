class Product:
    def __init__(self, main_link: str, other_links: dict, title: str,
                 price: dict, image: str, specifications: dict):
        self.main_link = main_link                 # DigiKala link
        self.links = other_links                   # {site name: link}
        self.title = title
        self.price = price                         # {site name: str or "Unavailable"}
        self.image = image                         # image path
        self.specifications = specifications       # {'title': list[str], 'info': list[str]}

    def check_link(self, link: str):
        """This method checks existence of given link in Product links (main and other links)"""
        if link == self.main_link or link in self.links:
            return False
        else:
            return True

    def update_price(self, site: str, new_price: str | None):
        if type(new_price) == str: self.price[site] = new_price

    def get_informations(self):
        return {
            "main_link": self.main_link, "other_links": self.links, "title": self.title, "price": self.price,
            "image": self.image, "specifications": self.specifications
        }