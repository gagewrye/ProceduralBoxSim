import java.util.Arrays;


// Comparable Minimum Heap backed by an Array.
public class MinHeap<T extends Comparable> {

    protected final int DEFAULT_CAPACITY = 30;
    protected int size;
    protected Comparable[] array;

    // initializes an empty MinHeap.
    public MinHeap() {
        this.size = 0;
        this.array = (T[]) new Comparable[DEFAULT_CAPACITY + 1];
    }

    public MinHeap(int capacity) {
        this.size = 0;
        this.array = (T[]) new Comparable[capacity + 1];
    }

    /***
     * Build heap from given array.
     * @param heapArray Array from which to build heap
     */
    public void buildHeap(T[] heapArray) {
        this.size = heapArray.length;

        // creates new larger array and copies input array.
        Comparable[] newArray = new Comparable[heapArray.length + 1];
        System.arraycopy(heapArray, 0, newArray, 1, heapArray.length);

        this.array = newArray;
        for (int index = this.size / 2; 0 < index; index--) {
            this.heapify(index);
        }
    }

    /* Returns the index of the left child of the element at index. */
    public int getLeftOf(int index) {
        return 2 * index;
    }

    /* Returns the index of the right child of the element at index. */
    public int getRightOf(int index) {
        return (2 * index) + 1;
    }

    /* Returns the index of the parent of the element at index. */
    public int getParentOf(int index) {
        return index / 2;
    }

    public void swap(int index1, int index2) {
        Comparable element1 = this.array[index1];
        this.array[index1] = this.array[index2];
        this.array[index2] = element1;
    }

    /* Performs bubbleUp and bubbleDown to correct the heap array */
    protected void heapify(int index) {
        int leftIndex = this.getLeftOf(index);
        int rightIndex = this.getRightOf(index);

        if (rightIndex <= this.size) {
            int smallestIndex;
            if (this.array[leftIndex].compareTo(this.array[rightIndex]) > 0) {
                smallestIndex = rightIndex;
            } else {
                smallestIndex = leftIndex;
            }

            if (this.array[index].compareTo(this.array[smallestIndex]) > 0) {
                this.swap(index, smallestIndex);
                this.heapify(smallestIndex);
            }

        } else if (leftIndex == this.size
                && this.array[index].compareTo(this.array[leftIndex]) > 0) {
            this.swap(index, leftIndex);
        }
    }

    /* Inserts a new value to the heap. */
    public void insert(T value) {
        this.size++;
        int index = this.size;

        while (index > 1 && this.array[this.getParentOf(index)].compareTo(value) > 0) {
            this.array[index] = this.array[this.getParentOf(index)];
            index = this.getParentOf(index);
        }
        this.array[index] = value;
    }

    /***
     * Decrease the value of the node at index by replacing its value with new value.
     * @param index Location of the node.
     * @param newValue value that is smaller than the node's existing value.
     */
    protected void decreaseKey(int index, T newValue) {
        if (this.array[index] == null) {
            return;
        }
        if (this.array[index].compareTo(newValue) <= 0) {
            this.array[index] = newValue;
            this.heapify(1);
        }
    }

    public boolean isEmpty() {return this.size == 0;}

    /* Returns the number of elements in the MinHeap. */
    public int size() {return this.size;}

    /* Returns and removes the smallest element in the MinHeap. */
    public T removeMin() {
        Comparable minimum = this.array[1];
        // pull end of array to the top
        this.array[1] = this.array[size];
        size--;
        this.heapify(1); // bubbleDown
        return (T) minimum;
    }

    public boolean contains(T element) {
        return Arrays.asList(array).contains(element);
    }
}