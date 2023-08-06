# A Python formatter from formats like rst and markdown to the content tree

## Source
Объект для обращения с источником документов
 
Принимает на вход строку с указанием адресса ресурса + путь к материалам относительно корня документа

source = Source(url, path)

## Parser
Объект, предоставляющий интерфейс для обращения к дереву 

Работает как дескриптор

tree = Parser(source)

## Formatter
Объект для преобразования сырого дерева. Для чистки от символов формата и присвоения типов

done_tree = Formatter(tree)

## Преобразование дерева в json
done_tree.to_json()
