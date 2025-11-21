using System;
using System.Diagnostics;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;

namespace IMS.Services
{
    public static class ApiClient
    {
        // Single shared HttpClient instance
        public static HttpClient _client;
        private static HttpClientHandler _handler;  // ✅ Add this line


        static ApiClient()
        {
            _handler = new HttpClientHandler()
            {
                UseCookies = true, // store cookies!
                CookieContainer = new CookieContainer(),
                AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate,
            };

            _client = new HttpClient(_handler);

            // base URL (optional, can use full URLs too)
            _client.BaseAddress = new Uri("http://localhost:8000/");

            // default headers
            _client.DefaultRequestHeaders.Accept.Clear();
            _client.DefaultRequestHeaders.Accept.Add(
                new MediaTypeWithQualityHeaderValue("application/json"));
        }

        public static void PrintCookies()
        {
            var cookies = _handler.CookieContainer.GetCookies(new Uri("http://localhost:8000/"));
            foreach (Cookie cookie in cookies)
            {
                Console.WriteLine($"🍪 {cookie.Name} = {cookie.Value}");
            }
        }

        // Generic POST

        public static async Task<T?> PostAsync<T>(string url, object payload)
        {
            try
            {
                var response = await _client.PostAsJsonAsync(url, payload);
                Debug.WriteLine($"➡️ POST {url} -> {response.StatusCode}");
                PrintCookies();

                if (!response.IsSuccessStatusCode)
                {
                    var text = await response.Content.ReadAsStringAsync();
                    Debug.WriteLine($"Failed: {text}");
                   return default;
                }

                return await response.Content.ReadFromJsonAsync<T>();
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Exception in postasync: {ex.Message}");
                return default;
            }
        }



        // Generic GET
        public static async Task<T?> GetAsync<T>(string url)
        {
            try
            {
                HttpResponseMessage response = await _client.GetAsync(url);
                Console.WriteLine($"➡️ GET {url} -> {response.StatusCode}");
                PrintCookies();
                if (!response.IsSuccessStatusCode)
                    return default;

                return await response.Content.ReadFromJsonAsync<T>();
            }
            catch(Exception ex)
            {
                Console.WriteLine($"❌ Exception in GetAsync: {ex.Message}");
                return default;
            }
        }

        public static async Task<bool> DeleteAsync(string url)
        {
            try
            {
                var response = await _client.DeleteAsync(url);
                return response.IsSuccessStatusCode;
            }
            catch
            {
                return false;
            }
        }

    }

}
