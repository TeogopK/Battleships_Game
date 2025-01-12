using ShipDataManagement.Models;

namespace ShipDataManagement.Services;

public interface IFakeDbOperations
{
    public Task<bool> AddAsync(StatsEntityRequest statsEntity);

    public Task<StateEntityResponse> GetAsync();
}
