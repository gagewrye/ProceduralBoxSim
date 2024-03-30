import byow.Core.Objects.PrimObject;

// PrimObject version of MinHeap, used in Prim's algorithm implementation

public class PrimObjectHeap extends MinHeap<PrimObject> {

    // When item is not in the heap
    private final int EMPTY = -1;

    // Locations in the heap
    private int[] locations;

    public PrimObjectHeap(int capacity) {
        super(capacity);
        initializeLocations(capacity);

    }

    public PrimObjectHeap() {
        super();
        initializeLocations(DEFAULT_CAPACITY);
    }

    private void initializeLocations(int capacity) {
        this.locations = new int[capacity + 1];
        for (int i = 0; i < locations.length; i++) {
            this.locations[i] = EMPTY;
        }
    }

    @Override
    public void swap(int first, int second) {
        super.swap(first, second);
        PrimObject firstObj = (PrimObject) this.array[first];
        PrimObject secondObj = (PrimObject) this.array[second];

        int temp = this.locations[secondObj.getIndex()];
        this.locations[secondObj.getIndex()] = this.locations[firstObj.getIndex()];
        this.locations[firstObj.getIndex()] = temp;
    }

    @Override
    public void insert(PrimObject value) {
        this.size++;
        int index = this.size;
        this.locations[value.getIndex()] = size;

        while (index > 1 && this.array[this.getParentOf(index)].compareTo(value) > 0) {
            // Keep track of the locations here
            int temp = this.locations[getParentOf(index)];
            this.locations[getParentOf(index)] = this.locations[index];
            this.locations[index] = temp;

            // Go up
            this.array[index] = this.array[this.getParentOf(index)];
            index = this.getParentOf(index);
        }

        this.array[index] = value;
        this.locations[value.getIndex()] = index;
    }

    /**
     *
     * Update Prim Objects location in the heap
     *
     * @param object Prim object with new value
     */
    public void update(PrimObject object) {
        int heapLocation = this.locations[object.getIndex()];
        this.decreaseKey(heapLocation, object);
    }

    /**
     *
     * Returns true if the object is in the heap
     *
     * @param object PrimObject to check
     * @return True if object is in the heap, false if not
     */
    public boolean contains(PrimObject object) {
        return locations[object.getIndex()] != EMPTY;
    }

    /***
     * Returns copy of the internal array used in heap
     * @return Heap array
     */
    public Comparable[] getArray() {
        return array.clone();
    }

    /***
     * Returns array containing locations of the prim objects
     * @return Array containing locations of the prim objects
     */
    public int[] getHeapLocations() {
        return locations.clone();
    }

    @Override
    public PrimObject removeMin() {
        PrimObject minimum = (PrimObject) this.array[1];

        // Locations is set first because the index
        int first  = ((PrimObject) this.array[1]).getIndex();
        int second = ((PrimObject) this.array[this.size]).getIndex();
        this.locations[first] = EMPTY;
        this.locations[second] = 1;

        // Add bottom to top
        this.array[1] = this.array[this.size];
        this.array[this.size] = null;

        // Remove from track
        this.locations[minimum.getIndex()] = EMPTY;
        this.size--;

        // Fix minheap
        this.heapify(1);

        return minimum;
    }

}