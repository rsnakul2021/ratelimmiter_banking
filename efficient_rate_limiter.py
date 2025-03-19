from collections import defaultdict #default dict for an efficient data structure
import time

#implementing fixed window - simple and leaky bucket - timestamp based
fixed_window_storage = defaultdict(lambda: {'window': 0, 'count': 0})
leaky_bucket_storage = defaultdict(lambda: {'last_time': time.time(), 'level': 0.0})

def fixed_window_allow(user_id, max_requests=5, window_size=1):
    current_time = time.time()
    current_window = int(current_time / window_size)
    user_data = fixed_window_storage[user_id]
    if user_data['window'] != current_window:
        user_data.update({'window': current_window, 'count': 0})
    if user_data['count'] < max_requests:
        user_data['count'] += 1
        return True
    return False

def leaky_bucket_allow(user_id, capacity=5, leak_rate=1):
    current_time = time.time()
    user_data = leaky_bucket_storage[user_id]
    time_passed = current_time - user_data['last_time']
    new_level = max(0, user_data['level'] - (time_passed * leak_rate))
    user_data['last_time'] = current_time
    user_data['level'] = new_level
    if new_level < capacity:
        user_data['level'] += 1
        return True
    return False

def test_rate_limiter(limiter_func, name):
    print(f"\n{name}")
    print("Requests:")
    for i in range(7):
        result = limiter_func("test_user")
        print(f"Request {i+1}: {'Transaction Good' if result else 'Transaction Blocked'}")
    print("\nPassing 2 seconds:")
    time.sleep(2)
    print("Testing 3 more requests:")
    for i in range(3):
        result = limiter_func("test_user")
        print(f"Request {i+1}: {'Transaction Good' if result else 'Transaction Blocked'}")

if __name__ == "__main__":
    print("Fixed Window:")
    test_rate_limiter(lambda user_id: fixed_window_allow(user_id, max_requests=5, window_size=1), "Fixed Window Rate Limiter")
    print("\nLeaky Bucket:")
    test_rate_limiter(lambda user_id: leaky_bucket_allow(user_id, capacity=5, leak_rate=1), "Leaky Bucket Rate Limiter") 