# Use the official .NET 8 SDK image as a build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app

# Copy project files and restore dependencies
COPY ShipDataManagement.csproj .
RUN dotnet restore

# Copy the entire application source code
COPY . .

# Build the application
RUN dotnet publish -c Release -o /app/out

# Use the official .NET 8 runtime image for the final stage
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app

# Copy the published output from the build stage
COPY --from=build /app/out .

EXPOSE 5099

ENV ASPNETCORE_URLS=http://+:5099

# Set the entry point for the container
ENTRYPOINT ["dotnet", "ShipDataManagement.dll"]
