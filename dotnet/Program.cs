using TradingMcp.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddSingleton<IDocumentIndex, DocumentIndex>();

var app = builder.Build();

app.MapGet("/", (IDocumentIndex index) =>
    Results.Ok(new { name = "trading-mcp-csharp", documents = index.Count }));

app.MapGet("/documents", (IDocumentIndex index) =>
    Results.Ok(index.GetAll().Select(d => new { id = d.Id, filename = d.Filename })));

app.MapGet("/document/{id:int}", (int id, IDocumentIndex index) =>
{
    var doc = index.GetById(id);
    return doc is null
        ? Results.NotFound(new { error = "not found" })
        : Results.Ok(new { id = doc.Id, filename = doc.Filename, text = doc.Text });
});

app.MapGet("/search", (IDocumentIndex index, string? q, int limit = 10) =>
{
    if (string.IsNullOrWhiteSpace(q))
        return Results.Ok(Array.Empty<object>());

    return Results.Ok(index.Search(q, limit));
});

app.Run();
