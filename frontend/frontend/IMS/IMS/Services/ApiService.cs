using IMS.Models;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;
using System.Threading.Tasks;
using static IMS.Windows.LoginWindow;

namespace IMS.Services
{
    public static class ApiService
    {
        private static readonly CookieContainer _cookies = new CookieContainer();
        private static readonly HttpClient _client;
        private static HttpClientHandler _handler;  


        static ApiService()
        {
            _handler = new HttpClientHandler()
            {
                UseCookies = true,
                CookieContainer = _cookies,
                AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate,
            };

            _client = new HttpClient(_handler)
            {
                BaseAddress = new Uri("http://localhost:8000/")
            };

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

        // ------------------------------
        // LOGIN
        public static async Task<bool> LoginAsync(string username, string password)
        {
            var payload = new { username, password };
            var response = await _client.PostAsJsonAsync("auth/login", payload);
            if (!response.IsSuccessStatusCode)
            {
                Console.WriteLine("❌ Login failed");
                return false;
            }

            PrintCookies();

            Debug.WriteLine("✅ Login succeeded");
    //        var cookies = ((HttpClientHandler)_handler).CookieContainer
    //.GetCookies(new Uri("http://localhost:8000/"));

    //        foreach (Cookie cookie in cookies)
    //            Console.WriteLine($"🍪 Cookie stored: {cookie.Name} = {cookie.Value}");


            // HttpClientHandler is already storing cookies automatically
            return true;
        }


        // ------------------------------
        // COOKIE SET
        //public static void SetAuthCookie(string name, string value, string domain)
        //{
        //    _cookies.Add(new Cookie(name, value) { Domain = domain });
        //}

        // ------------------------------
        // STORES
        public static async Task<List<(string store, List<string> substores)>> GetStoresAsync()
        {
            var resp = await _client.GetAsync("ledger/");
            resp.EnsureSuccessStatusCode();

            var json = await resp.Content.ReadAsStringAsync();
            var raw = JsonConvert.DeserializeObject<List<dynamic>>(json);

            var result = new List<(string store, List<string> subs)>();
            foreach (var r in raw)
            {
                // Match backend keys
                string store = r.store_name ?? "";
                List<string> subs = new();

                try
                {
                    foreach (var s in r.ledgers)
                    {
                        subs.Add((string)s.Ledger_name); // from your backend response
                    }
                }
                catch { }

                result.Add((store, subs));
            }

            return result;
        }


        // ------------------------------
        // LEDGER GET (equipment pages)
        // ------------------------------
        public static async Task<List<LedgerItem>> GetLedgerAsync(string ledger_code)
        {
            var resp = await _client.GetAsync($"/ledger/?ledger_code={ledger_code}");
            resp.EnsureSuccessStatusCode();

            return await resp.Content.ReadFromJsonAsync<List<LedgerItem>>() ?? new();
        }

        // ------------------------------
        // LEDGER CREATE
        // ------------------------------
        public static async Task<LedgerItem?> CreateLedgerAsync(LedgerItem item)
        {
            var resp = await _client.PostAsJsonAsync($"/ledger/?ledger_code={item.Ledger_code}", item);
            resp.EnsureSuccessStatusCode();
            return await resp.Content.ReadFromJsonAsync<LedgerItem>();
        }

        // ------------------------------
        // LEDGER UPDATE
        // ------------------------------
        public static async Task<LedgerItem?> UpdateLedgerAsync(string pageName, LedgerItem item)
        {
            var resp = await _client.PutAsJsonAsync($"/ledger/?ledger_code={item.Ledger_code}", item);
            resp.EnsureSuccessStatusCode();
            return await resp.Content.ReadFromJsonAsync<LedgerItem>();
        }

        //// ------------------------------
        //// ADD PAGE TO EQUIPMENT
        //// ------------------------------
        //public static async Task<bool> AddPageAsync(string equipment, LedgerItem page)
        //{
        //    var resp = await _client.PostAsJsonAsync($"/", page);
        //    resp.EnsureSuccessStatusCode();
        //    return true;
        //}

        // ------------------------------
        // GENERIC GET
        // ------------------------------
        public static async Task<T?> GetAsync<T>(string endpoint)
        {
            var resp = await _client.GetAsync(endpoint);
            resp.EnsureSuccessStatusCode();

            return await resp.Content.ReadFromJsonAsync<T>();
        }

        // ------------------------------
        // GENERIC POST
        // ------------------------------
        public static async Task<T?> PostAsync<T>(string endpoint, object body)
        {
            var resp = await _client.PostAsJsonAsync(endpoint, body);
            resp.EnsureSuccessStatusCode();

            return await resp.Content.ReadFromJsonAsync<T>();
        }

        // ------------------------------
        // GENERIC DELETE
        // ------------------------------
        public static async Task DeleteAsync(string endpoint)
        {
            var resp = await _client.DeleteAsync(endpoint);
            resp.EnsureSuccessStatusCode();
        }


    }
}
