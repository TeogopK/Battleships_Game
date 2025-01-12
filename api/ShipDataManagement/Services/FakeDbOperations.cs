using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Npgsql;
using NpgsqlTypes;
using ShipDataManagement.Models;

namespace ShipDataManagement.Services;

public class FakeDbOperations(IConfiguration configuration, ILogger<FakeDbOperations> logger) : IFakeDbOperations
{
    private int inMemoryRome = 0;
    private int intMemoryCarthage = 0;

    public async Task<StateEntityResponse> GetAsync()
    {
        StateEntityResponse state = new StateEntityResponse() { Id = 42, Rome = inMemoryRome, Carthage = intMemoryCarthage };

        return state;
    }

    public async Task<bool> AddAsync(StatsEntityRequest statsEntity)
    {
        if (statsEntity.Win == 1)
        {
            intMemoryCarthage++;
        }
        else
        {
            inMemoryRome++;
        }
        return true;
    }
}
