using System;
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

        static ApiClient()
        {
            var handler = new HttpClientHandler()
            {
                UseCookies = true, // store cookies!
                CookieContainer = new CookieContainer(),
                AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate,
            };

            _client = new HttpClient(handler);

            // base URL (optional, can use full URLs too)
            _client.BaseAddress = new Uri("http://localhost:8000/");

            // default headers
            _client.DefaultRequestHeaders.Accept.Clear();
            _client.DefaultRequestHeaders.Accept.Add(
                new MediaTypeWithQualityHeaderValue("application/json"));
        }

        // Generic POST

        public static async Task<T?> PostAsync<T>(string url, object payload)
        {
            try
            {
                var response = await _client.PostAsJsonAsync(url, payload);


                if (!response.IsSuccessStatusCode)
                {
                    var text = await response.Content.ReadAsStringAsync();
                    return default;
                }

                return await response.Content.ReadFromJsonAsync<T>();
            }
            catch (Exception ex)
            {

                return default;
            }
        }



        // Generic GET
        public static async Task<T?> GetAsync<T>(string url)
        {
            try
            {
                HttpResponseMessage response = await _client.GetAsync(url);

                if (!response.IsSuccessStatusCode)
                    return default;

                return await response.Content.ReadFromJsonAsync<T>();
            }
            catch
            {
                return default;
            }
        }
    }
}
