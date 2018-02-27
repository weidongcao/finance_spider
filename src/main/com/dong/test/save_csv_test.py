"""
将爬虫爬取的数据保存为CSV文件
"""
import csv
with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    writer.writerow(['id', 'name', 'age'])
    writer.writerow(['1001', 'Mike', 20])
    writer.writerow(['1002', 'Dong', 28])
    writer.writerow(['1003', 'Poem', 27])

print('------------------ 字典写入 ------------------------')
with open('dict.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['id', 'name', 'age']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'id': '1001', 'name': 'Mike', 'age': 20})
    writer.writerow({'id': '1002', 'name': 'Dong', 'age': 28})
    writer.writerow({'id': '1003', 'name': 'Poem', 'age': 27})
