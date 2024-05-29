class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def array_to_linked_list(self, arr):
        for item in arr:
            self.add_to_end(item)

    def add_to_front(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def add_to_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")

    def linked_list_to_array(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

# # Example usage
# arr = [1, 2, 3, 4, 5]
# linked_list = LinkedList()
# linked_list.array_to_linked_list(arr)
# linked_list.display()

# linked_list.add_to_front(0)
# linked_list.display()

# linked_list.add_to_end(6)
# linked_list.display()

# array_from_linked_list = linked_list.linked_list_to_array()
# print(array_from_linked_list)

