import requests
from bs4 import BeautifulSoup
import re
import time
import simplejson
from collections import defaultdict,Counter


home_page_link = 'https://orangecounty.craigslist.org/'


def soupify(link):
    requested = requests.get(link)
    soup = BeautifulSoup(requested.text,'html.parser')
    return soup

def tags_to_extract(soup,tag,id_dic,deeper_tag):
    key = ''
    value = ''
    for k,v in id_dic.items():
        key = k
        value = v
    first_level = soup.find(tag,{key:value})
    return first_level.find_all(deeper_tag)


def transform_link(link):
    temp_link = home_page_link
    temp_link += link
    return temp_link


def sale_extract(soup,tag,*class_info):
    if len(class_info) > 2:
        return sale_soup.findAll('a', {'class': [class_info[0],class_info[1]]})
    else:
        return soup.find_all(tag,class_ = class_info)

    #return sale_soup.findAll('a', {'class': ['result-image gallery','result-image gallery empty']}))
def clean_list(dirty_list):
    cleaned_list = []
    for element in dirty_list:
        element = re.sub('[^0-9a-zA-Z]+',' ', element)
        cleaned_list.append(element.lower())
    return cleaned_list


def clean_price_list(dirty_list):
    cleaned_list = []
    for element in dirty_list:
        try:
            element = re.sub('[^0-9a-zA-Z]+','', element)
            element = int(element)
            cleaned_list.append(element)
        except:
            cleaned_list.append('not being added')
    return cleaned_list

def tag_to_dict(tag_list1,tag_list2):
    item_list = clean_list([i.get_text() for i in tag_list1])
    price_list = clean_price_list([i.get_text() for i in tag_list2])
    export_to_database = {i:v for i,v in zip(item_list,price_list) if v!='not being added'}
    return export_to_database

def count_items(item_list,mode):
    counting_dic = defaultdict(int)
    if mode == 's':
        for i in item_list:
            list_count = Counter(i.split(' '))
            for k,v in list_count.items():
                counting_dic[k]+=v
    if mode == 'j':
        for i in item_list.values():
            for words in i:
                for sub_words in words.split(' '):
                    counting_dic[sub_words]+=1
    return counting_dic

def write_to_file(category_name,input):
    file_to = open('output/'+heyUser+'/'+category_name+'.txt','a+')
    for item in input:
        file_to.write(item)
        file_to.write('\n')
    file_to.write('\nNEXT\n')
    file_to.close()

def turn_page(link):
    next_link = transform_link(link.get('href')[1:])
    new_soup = soupify(next_link)
    return new_soup

def sale_run(ready_to_go_soup):
    for link in ready_to_go_soup:
        category_name = link.get_text().replace('/','')
        sold_soup = turn_page(link)
        test_sale_soup = sale_extract(sold_soup,'a','result-title hdrlnk') #Item being sold name
        price_sale_soup = sale_extract(sold_soup,'a',('result-image gallery','result-image gallery empty'))
        export_out = tag_to_dict(test_sale_soup,price_sale_soup)
        #print(count_items(export_out,heyUser))
        write_to_file(category_name,export_out)

def job_run(ready_to_go_soup):
    for link in ready_to_go_soup:
        category_name = link.get_text().replace('/','')
        page_job_soup = turn_page(link)
        job_a_list = sale_extract(page_job_soup,'a','result-title')
        cleaned_jobs = clean_list([j.get_text() for j in job_a_list])
        job_export = defaultdict(list)
        for i in cleaned_jobs:
            job_export[category_name].append(i)

        write_to_file(category_name,cleaned_jobs)

if __name__ == '''__main__''':
        soup = soupify(home_page_link)
        heyUser = input("Sale Build or Job Build: ").lower()

        if 's' == heyUser.lower():
            sale_run(tags_to_extract(soup,'ul',{'id':'sss0'},'a')) #Left for sale
            sale_run(tags_to_extract(soup,'ul',{'id':'sss1'},'a')) #Right for sale

        if 'j' == heyUser.lower():
            job_run(tags_to_extract(soup,'ul',{'id':'jjj0'},'a'))




        #keyword = 'software'
        #keyword1 = 'government'
        #for link in job_links:
        #    if (keyword in link.get_text() or keyword1 in link.get_text()):
        #        next_link = trasnform_link(link.get('href'))
        #        second_request = requests.get(next_link)
        #        second_text = second_request.text
        #        second_soup = BeautifulSoup(second_text,'html.parser')
        #        print(second_soup)
