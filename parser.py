from scrapy.selector import Selector
import os 

def read_file():
    file = open('data/CoreIdeasGlossaryTheses1stDraftPublic.html',mode='r')
    return file.read()

def clean_string(s):
    return s.replace(u'\xa0', u' ').strip()

def extract_title(content):
    data = Selector(text=content).xpath("//span[@class='c0' or @class='c1']//text()").extract()
    if len(data) > 0:
        return True, clean_string(data[0]).lower()
    return False, ""

def extract_text(content):
    text = Selector(text=content).xpath("//span/text()").extract()
    text = [tmp.lower() for tmp in text]

    if len(text) > 0:
        return [''.join(text)]

    return []

def extract_link(content):
    link = Selector(text=content).xpath("//span/@href").extract()
    link = [tmp for tmp in link if 'cmnt' not in tmp]
    return link

def extract_image(content):
    img = Selector(text=content).xpath("//img/@src").extract()
    return ["![[" + tmp + "]]" for tmp in img]

def save_concept(l):
    title = l[0].replace('/', '-')

    os.makedirs("nosilverv", exist_ok=True)
    fo = open(f'nosilverv/{title}.md', mode='w+')

    fo.write("#nosilverv \n")
    for tmp in l[1:]:
        fo.write(tmp + "\n")

    fo.close()

def parse():
    text = read_file()
    
    concept = [] 

    for paragraph in Selector(text=text).xpath("//p[not(contains(@class,'c15')) and not(contains(@class,'c16'))]").extract():
        is_title, content = extract_title(paragraph)
        if is_title:
            if len(concept) > 0:
                save_concept(concept)
                concept = []

            concept.append(content)
        else:
            concept.extend(extract_text(paragraph))
            concept.extend(extract_link(paragraph))
            concept.extend(extract_image(paragraph))


if __name__ == '__main__':
    parse()
