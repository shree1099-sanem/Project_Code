from turtledemo.sorting_animate import partition


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid= len(arr)//2
    left=merge_sort(arr[:mid])
    right=merge_sort(arr[mid:])
    print(f"Dividing: {arr} → {left} and {right}")

    return  merge(left,right)
def merge(left,right):
    l=[]
    left_idx=0
    right_idx = 0

    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] < right[right_idx]:
            l.append(left[left_idx])
            left_idx +=1
        else:
            l.append(right[right_idx])
            right_idx += 1
    l.extend(left[left_idx:])
    l.extend(right[right_idx:])
    return l
    print(f"Merged: {left} and {right} → {arr}")


arr=[38,27,43,3,9,82,10]
print(merge_sort(arr))

print("/////////////////////////////////////////////////////////////////////////////////////")

def quick_sort(arr,low=0,high=None):
    if high is None:
        high=len(arr)-1
    if low < high:
        pivot_idx=partition(arr,low,high)
        print(f"Pivot placed at index {pivot_idx}: {arr}")

        quick_sort(arr,low,pivot_idx-1)
        quick_sort(arr,pivot_idx+1,high)
    return arr

def partition(arr,low,high):
    pivot = arr[high]
    i=low
    for j in range(low,high):
        if arr[j]<pivot:
            arr[i],arr[j] = arr[j],arr[i]
            i += 1
            print(f"Swapped {arr[i]} and {arr[j]}: {arr}")
    arr[i],arr[high] = arr[high],arr[i]
    print(f"Swapped pivot {arr[i + 1]} with {arr[high]}: {arr}")
    return i
arr=[10,7,8,9,1,5]
print("sorted",quick_sort(arr.copy()))




