from pprint import pprint
import re
import csv

def read_csv(file):
  with open(file, encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
  return contacts_list

def substitute_numbers(file):
  list = read_csv(file)
  for person in list:
    text = person[5]
    pattern = re.compile(r"(\+7|8)\s*\(*(\d{3})[\)|\-|\s]*(\d{3})\-?(\d{2})\-?(\d{2})\s*\(?(доб. \d*)*\)?")
    person[5] = pattern.sub(r"+7(\2)\3-\4-\5 \6", text)
    if len(person[5]) != 0:
      if person[5][-1] == ' ':
        person[5] = person[5].strip()
  return list

def separate_names(file):
  list = substitute_numbers(file)
  for person in list[1:]:
    if len(person[0].split(' ')) == 3:
      person[0:3] = person[0].split(' ')
    elif len(person[0].split(' ')) == 2:
      person[0:2] = person[0].split(' ')
    elif len(person[1].split(' ')) == 2:
      person[1:3] = person[1].split(' ')
  return list

def unite_dubles(file):
  list = separate_names(file)
  for p in range(1, len(list)-1):
    person = list[p]
    for i in range(3, len(person)):
      if person[i] == '':
        for second_p in range(p + 1, len(list)):
          second_person = list[second_p]
          if second_person[0] == person[0]:
            person[i] = second_person[i]
            break
  return list

def delete_doubles(file):
  list = unite_dubles(file)
  new_list = []
  for person in list:
    if person == list[0]:
      new_list.append(person)
    elif person == list[1]:
      new_list.append(person)
    else:
      check = True
      for dif_person in new_list:
        if person [0] == dif_person [0]:
          check = False
      if check == True:
        new_list.append(person)

  return new_list

def write_pretty_phonebook(file):
  with open(f'pretty_{file}', "w", encoding='cp1251') as f:
    datawriter = csv.writer(f, delimiter=',')
    pretty_phonebook = delete_doubles(file)
    datawriter.writerows(pretty_phonebook)

if __name__ == '__main__':

  write_pretty_phonebook("phonebook_raw.csv")
