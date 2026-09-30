using System.Collections.ObjectModel;
using System.Text.Json;
using System.Text.Json.Serialization;
using TradingMcp.Models;

namespace TradingMcp.Services;

internal sealed partial class DocumentIndex : IDocumentIndex
{
    private readonly ReadOnlyCollection<Document> _documents;
    private readonly ILogger<DocumentIndex> _logger;

    public DocumentIndex(ILogger<DocumentIndex> logger, IWebHostEnvironment env)
    {
        ArgumentNullException.ThrowIfNull(env);
        _logger = logger;
        _documents = LoadIndex(env.ContentRootPath);
    }

    public int Count => _documents.Count;

    public IReadOnlyList<Document> GetAll() => _documents;

    public Document? GetById(int id) =>
        _documents.FirstOrDefault(d => d.Id == id);

    public IReadOnlyList<SearchResult> Search(string query, int limit) =>
        _documents
            .Select(d => new SearchResult(
                d.Id,
                d.Filename,
                CountOccurrences(d.Text, query),
                BuildSnippet(d.Text, query)))
            .Where(r => r.Score > 0)
            .OrderByDescending(r => r.Score)
            .Take(limit)
            .ToList();

    private ReadOnlyCollection<Document> LoadIndex(string contentRoot)
    {
        var indexPath = Path.Combine(contentRoot, "data", "index.json");

        if (!File.Exists(indexPath))
        {
            LogIndexNotFound(_logger, indexPath);
            return new ReadOnlyCollection<Document>([]);
        }

        try
        {
            var json = File.ReadAllText(indexPath);
            var raw = JsonSerializer.Deserialize<List<RawDocument>>(json) ?? [];

            return raw
                .Select((d, i) => new Document
                {
                    Id       = d.Id ?? i,
                    Filename = d.Filename ?? string.Empty,
                    Path     = d.Path,
                    Text     = d.Text ?? string.Empty
                })
                .ToList()
                .AsReadOnly();
        }
        catch (JsonException ex)
        {
            LogLoadFailed(_logger, ex, indexPath);
            return new ReadOnlyCollection<Document>([]);
        }
        catch (IOException ex)
        {
            LogLoadFailed(_logger, ex, indexPath);
            return new ReadOnlyCollection<Document>([]);
        }
    }

    [LoggerMessage(Level = LogLevel.Warning, Message = "Index file not found at {Path}")]
    private static partial void LogIndexNotFound(ILogger logger, string path);

    [LoggerMessage(Level = LogLevel.Error, Message = "Failed to load index from {Path}")]
    private static partial void LogLoadFailed(ILogger logger, Exception ex, string path);

    private static int CountOccurrences(string text, string query)
    {
        int count = 0, index = 0;
        while ((index = text.IndexOf(query, index, StringComparison.OrdinalIgnoreCase)) != -1)
        {
            count++;
            index += query.Length;
        }
        return count;
    }

    private static string BuildSnippet(string text, string query, int radius = 120)
    {
        if (string.IsNullOrEmpty(text))
            return string.Empty;

        var idx = text.IndexOf(query, StringComparison.OrdinalIgnoreCase);
        if (idx == -1)
            return text.Length <= radius * 2
                ? text
                : string.Concat(text.AsSpan(0, radius * 2), "...");

        var start  = Math.Max(0, idx - radius);
        var end    = Math.Min(text.Length, idx + query.Length + radius);
        var prefix = start > 0 ? "..." : string.Empty;
        var suffix = end < text.Length ? "..." : string.Empty;

        return string.Concat(prefix, text[start..end].Trim(), suffix);
    }

    // DTO used only for JSON deserialization; not exposed outside this class.
    private sealed class RawDocument
    {
        [JsonPropertyName("id")]      public int?    Id       { get; init; }
        [JsonPropertyName("filename")] public string? Filename { get; init; }
        [JsonPropertyName("path")]    public string? Path     { get; init; }
        [JsonPropertyName("text")]    public string? Text     { get; init; }
    }
}
