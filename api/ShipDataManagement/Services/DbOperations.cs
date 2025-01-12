using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Npgsql;
using NpgsqlTypes;
using ShipDataManagement.Models;

namespace ShipDataManagement.Services;

public class DbOperations(IConfiguration configuration, ILogger<DbOperations> logger) : IDbOperations
{
    public async Task<StateEntityResponse> GetAsync()
    {
        var statsList = new List<StateEntityResponse>();

        using (var connection = new NpgsqlConnection(configuration.GetConnectionString("postgreSQL")))
        {
            await connection.OpenAsync();

            using (var command = new NpgsqlCommand("SELECT * FROM stats limit 1", connection))
            {
                using (var reader = await command.ExecuteReaderAsync())
                {
                    while (await reader.ReadAsync())
                    {
                        var stats = new StateEntityResponse
                        {
                            Id = Convert.ToInt32(reader["id"]),
                            Rome = Convert.ToInt32(reader["red"]),
                            Carthage = Convert.ToInt32(reader["blue"])
                        };

                        statsList.Add(stats);
                    }
                }
            }
        }

        return statsList.FirstOrDefault<StateEntityResponse>();
    }


    public async Task<bool> AddAsync(StatsEntityRequest statsEntity)
    {

        StateEntityResponse first = await GetAsync();

        if (statsEntity.Win == 1)
        {
            first.Carthage++;
        }
        else
        {
            first.Rome++;
        }

        long result = 0;
        const string sql = "UPDATE public.stats SET red = @r, blue = @b WHERE id = @id";

        try
        {
            using (NpgsqlConnection connection = new NpgsqlConnection(configuration.GetConnectionString("postgreSQL")))
            {
                await connection.OpenAsync();

                using (NpgsqlCommand command = new NpgsqlCommand(sql, connection))
                {
                    command.Parameters.Add(new NpgsqlParameter("id", NpgsqlDbType.Integer) { Value = first.Id });
                    command.Parameters.Add(new NpgsqlParameter("r", NpgsqlDbType.Integer) { Value = first.Rome });
                    command.Parameters.Add(new NpgsqlParameter("b", NpgsqlDbType.Integer) { Value = first.Carthage });

                    result = await command.ExecuteNonQueryAsync();
                }
            }
            return true;
        }
        catch (Exception e)
        {
            logger.LogError("Insert failed: {Message}", e.Message);
        }

        return false;
    }
}
