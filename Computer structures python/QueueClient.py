
# Listing 4-6
from QueueExercise3 import Queue
queue = Queue(10)
for person in ['Don', 'Kelly', 'Ivan', 'Rita', 'Amir', 'Adele', 'Fredde grädde', 'Ogginator', 'bla', 'mjau']:
    queue.insert(person)
print('After inserting', len(queue),
'persons in the queue it contains:\n', queue)
print('First in queue:', queue.peek())
print('Is queue full?', queue.is_full())
print('Removing items from the queue')
while not queue.is_empty():
    print(queue.remove(), end= ' ')
print()
