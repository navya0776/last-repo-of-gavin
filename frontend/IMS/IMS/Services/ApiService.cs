using IMS.Models;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
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

        static ApiService()
        {
            var handler = new HttpClientHandler()
            {
                UseCookies = true,
                CookieContainer = _cookies,
                AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate,
            };

            _client = new HttpClient(handler)
            {
                BaseAddress = new Uri("http://localhost:8000/")
            };

            _client.DefaultRequestHeaders.Accept.Clear();
            _client.DefaultRequestHeaders.Accept.Add(
                new MediaTypeWithQualityHeaderValue("application/json"));
        }

        // ------------------------------
        // LOGIN
        public static async Task<LoginResponse?> LoginAsync(string username, string password)
        {
            var payload = new { username, password };
            var resp = await _client.PostAsJsonAsync("/auth/login/", payload);

            if (!resp.IsSuccessStatusCode)
                return null;

            return await resp.Content.ReadFromJsonAsync<LoginResponse>();
        }

        // ------------------------------
        // COOKIE SET
        public static void SetAuthCookie(string name, string value, string domain)
        {
            _cookies.Add(new Cookie(name, value) { Domain = domain });
        }

        // ------------------------------
        // STORES
        public static async Task<List<(string store, List<string> substores)>> GetStoresAsync()
        {
            var resp = await _client.GetAsync("/stores");
            resp.EnsureSuccessStatusCode();

            var json = await resp.Content.ReadAsStringAsync();
            var raw = JsonConvert.DeserializeObject<List<dynamic>>(json);

            var result = new List<(string store, List<string> subs)>();
            foreach (var r in raw)
            {
                string store = r.store ?? r.name ?? "";
                List<string> subs = new();

                try { foreach (var s in r.substores) subs.Add((string)s); } catch { }

                result.Add((store, subs));
            }

            return result;
        }

        // ------------------------------
        // LEDGER GET
        public static async Task<List<LedgerItem>> GetLedgerAsync(string store, string substore)
        {
            var url = $"/ledger?store={WebUtility.UrlEncode(store)}&substore={WebUtility.UrlEncode(substore)}";
            var resp = await _client.GetAsync(url);

            resp.EnsureSuccessStatusCode();

            var json = await resp.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<List<LedgerItem>>(json) ?? new();
        }

        // ------------------------------
        // LEDGER CREATE
        public static async Task<LedgerItem?> CreateLedgerAsync(LedgerItem item)
        {
            var resp = await _client.PostAsJsonAsync("/ledger", item);
            resp.EnsureSuccessStatusCode();
            return await resp.Content.ReadFromJsonAsync<LedgerItem>();
        }

        // ------------------------------
        // LEDGER UPDATE
        public static async Task<LedgerItem?> UpdateLedgerAsync(Guid id, LedgerItem item)
        {
            var resp = await _client.PutAsJsonAsync($"/ledger/{id}", item);
            resp.EnsureSuccessStatusCode();
            return await resp.Content.ReadFromJsonAsync<LedgerItem>();
        }

        // ------------------------------
        // LEDGER DELETE
        public static async Task DeleteLedgerAsync(Guid id)
        {
            var resp = await _client.DeleteAsync($"/ledger/{id}");
            resp.EnsureSuccessStatusCode();
        }
    }
}
