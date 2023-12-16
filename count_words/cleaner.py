import re

class Cleaner:

    def __init__(self, text):
        self.text = text

    def remove_special_char(self, text):
        text = re.sub('[^a-zA-Z]+', " ", text)
        return re.sub('\d+', "", text)

    def ignore_case_sensitive(self, text):
        return text.lower()
    
    def clean(self):
        self.text = self.ignore_case_sensitive(self.text)
        return self.remove_special_char(self.text)
    