using TradingMcp.Models;

namespace TradingMcp.Services;

internal sealed record SearchResult(int Id, string Filename, int Score, string Snippet);

internal interface IDocumentIndex
{
    int Count { get; }
    IReadOnlyList<Document> GetAll();
    Document? GetById(int id);
    IReadOnlyList<SearchResult> Search(string query, int limit);
}
