using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using ShipDataManagement.Models;
using ShipDataManagement.Services;

namespace ShipDataManagement.Controllers
{
    [ApiController]
    [Route("management")]
    public class ManagementController(IConfiguration configuration, IFakeDbOperations dbOperations, ILogger<ManagementController> logger) : ControllerBase
    {
        [HttpGet("stats")]
        public async Task<StateEntityResponse> Get()
        {
            return await dbOperations.GetAsync();
        }

        [HttpPost("stats")]
        public async Task<bool> Post([FromBody] StatsEntityRequest stateEntity)
        {

            return await dbOperations.AddAsync(stateEntity);
        }
    }
}
