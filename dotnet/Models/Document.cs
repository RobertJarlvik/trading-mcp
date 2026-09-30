namespace TradingMcp.Models;

internal sealed record Document
{
    public int Id { get; init; }
    public string Filename { get; init; } = string.Empty;
    public string? Path { get; init; }
    public string Text { get; init; } = string.Empty;
}
