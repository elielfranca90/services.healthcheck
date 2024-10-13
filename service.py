import requests

# # Initialize with your existing services
# services = [
#     "http://consultatributos.com.br:8080/api/v1/public/GetStatusService"
# ]

# def check_services():
#     results = []
#     for service in services:
#         start_time = time.time()
#         try:
#             response = requests.get(service, timeout=10)
#             end_time = time.time()
#             total_time = end_time - start_time
#             service_quality = check_quality(response.status_code, total_time)
#             results.append({
#                 "url": service,
#                 "status_code": response.status_code,
#                 "response_time": f"{total_time:.4f}",
#                 "quality": service_quality
#             })
#             if service_quality == "Amazing":
#                 send_amazing_quality_email(service, f"{total_time:.4f}")
#         except requests.RequestException as e:
#             results.append({
#                 "url": service,
#                 "status_code": "Error",
#                 "response_time": "N/A",
#                 "quality": "Error"
#             })
#     return results