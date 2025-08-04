def linear_search(arr,target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
result=linear_search([10,20,30,40,50],30)
if result != -1:
    print(f"element found at index: {result}")
else:
    print("element not found")



def binary_search(arr,target):
    left=0
    right=len(arr)-1

    while left <= right:
        mid = (left+right)//2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left=mid+1
        else:
            right=mid-1
    return -1
res=binary_search([10,20,30,32,38,40,50,60,70],40)
if res != -1:
    print(f"element found at index: {res}")
else:
    print("element not found")