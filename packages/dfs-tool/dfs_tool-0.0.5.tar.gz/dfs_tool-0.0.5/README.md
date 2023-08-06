# dfs_tool

It is a HDFS cli tool. You can use it to manage your HDFS file system.

It calls the [WebHDFS](https://hadoop.apache.org/docs/r1.0.4/webhdfs.html) API.

# Configuration
You need to put a config file. By default, the config file is at `~/.dfs_tool/config.json`, however you can change it's location by setting environment variable `DFS_TOOL_CFG`

The configuration looks like below:
```json
{
    "api_base_uri": "https://my_hdfs_cluster.com/gateway/ui/webhdfs/v1/",
    "username": "superman",
    "password": "mypassword",
    "io_chunk_size": 16777216
}
```

* `api_base_url`: You need to put your WebHDFS endpoint here
* `username`: You need to specify your HDFS account username
* `password`: You need to specify your HDFS account password
* `io_chunk_size`: optional, if not set, the default value is 1048576. It is the chunk size for downloading data from HDFS or uploading data to HDFS, you may want to bump this value if your bandwidth is high

# Command supported
```
dfs_tool ls          <remote_path>                            -- list directory or file
dfs_tool download    <remote_filename> <local_path>           -- download file
dfs_tool cat         <remote_filename>                        -- cat a file
dfs_tool mkdir       <remote_dir_name>                        -- make a directory
dfs_tool rm -R       <remote_path>                            -- remove a file or directory
dfs_tool upload      <local_filename> <remote_path>           -- upload file
dfs_tool mv          <source_location> <destination_location> -- move file or directory
```