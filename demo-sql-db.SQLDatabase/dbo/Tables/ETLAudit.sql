CREATE TABLE [dbo].[ETLAudit] (
    [PipelineName] VARCHAR (50)  NULL,
    [StartTime]    DATETIME2 (7) NULL,
    [EndTime]      DATETIME2 (7) NULL,
    [Status]       VARCHAR (20)  NULL
);


GO

