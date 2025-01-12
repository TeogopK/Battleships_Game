using ShipDataManagement.Models;

namespace ShipDataManagement.Services;

public interface IDbOperations
{
    public Task<bool> AddAsync(StatsEntityRequest statsEntity);

    public Task<StateEntityResponse> GetAsync();
}
