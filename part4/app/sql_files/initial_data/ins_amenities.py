import uuid
amenities = ['WiFi', 'Swimming Pool', 'Air Conditioning']
for name in amenities:
    print(f"('{uuid.uuid4()}', '{name}')")
