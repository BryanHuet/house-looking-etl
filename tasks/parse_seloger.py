from prefect import task
from models.House import House
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import null


@task
def create_object(contents):
    fields = {"price": "sl.price-label",
              "title": "sl.title",
              "address": "sl.address",
              "photo": "sl.explore.PhotosContainer",
              "tags": "sl.tagsLine",
              "link": "sl.explore.coveringLink"}
    houses = []
    baseUrl = "https://www.seloger.com"
    for div in contents:
        photo = ''
        if (div.find(
                'div', {'data-testid': fields['photo']}).find(
                    'img') is not None):
            photo = div.find(
                'div', {'data-testid': fields['photo']}).find('img')['src']

        size = ''
        ground = ''

        link = ''
        if div.find('a', {'data-testid': fields['link']})['href'][0] != 'h':
            link = baseUrl+div.find('a',
                                    {'data-testid': fields['link']})['href']
        else:
            link = div.find('a', {'data-testid': fields['link']})['href']

        ul = div.find('ul', {'data-test': fields['tags']}).find_all('li')
        if (len(ul) > 2):
            size = div.find('ul',
                            {'data-test': fields['tags']}).find_all(
                                'li')[2].get_text()
        if (len(ul) > 3):
            ground = div.find('ul',
                              {'data-test': fields['tags']}).find_all(
                                  'li')[3].get_text()

        if size != '':
            size = size.replace('m²', ' ').replace(' ', '')
            size = int(size) if size.isnumeric() else null()
        else:
            size = null()

        if ground != '':
            ground = ground.replace(
                'Terrain', '').replace('m²', ' ').replace(' ', '')
            ground = int(ground) if ground.isnumeric() else null()
        else:
            ground = null()

        price = div.find('div', {'data-test': fields['price']}).get_text()
        price = int(price.replace('€', '').replace(' ', ''))
        houses.append(House(
            price=price,
            title=div.find('div', {'data-test': fields['title']}).get_text(),
            photo=photo if photo != '' else null(),
            address=div.find('div',
                             {'data-test': fields['address']}).get_text(),
            size=size,
            ground=ground,
            link=link if link != '' else null(),
        ))

    return houses


def object_exists(session, title, price, address, link):
    return session.query(House).filter_by(
        title=title, price=price,
        address=address, link=link).first() is not None


@task
def insert_new(engine, houses):
    Session = sessionmaker(bind=engine)
    session = Session()

    nb_inserted = 0
    for house in houses:
        if not object_exists(session, house.title, house.price,
                             house.address, house.link):
            session.add(house)
            nb_inserted = nb_inserted + 1

    session.commit()
    session.close()
    return nb_inserted
