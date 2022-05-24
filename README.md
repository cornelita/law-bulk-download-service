# LAW - BulkDownloadService

## Anggota - Kami Random

* 1806205041 - Timothy Regana Tarigan
* 1906306773 - Ghifari Aulia Azhar Riza
* 1906350830 - Muhammad Ikhsan Asa Pambayun
* 1906400261 - Jonathan Amadeus Hartman
* 1906292995 - Cornelita Lugita Santoso


## Prerequisites

* Docker


## How to run

1. Open terminal and run this command

    ```
    # Build
    docker compose build

    # Run
    docker compose up

    # Run - Detached
    docker compose up -d
    ```


## API Documentation

1. Ask to Download

    **URL**: {{base_url}}/bulk-download/

    **Method**: POST

    **Query Params**: None

    **Request Body**:
    | Parameter | Type          | Required? |
    |-----------|---------------|-----------|
    | videoIds  | Array[String] | yes       |

    **Example Response**:

    1. **OK**

        Request Body:

        ```
        {
            "videoIds": [
              "_8lJ5lp8P0U",
              "k_3DFCzcMC4"
            ]
        }
        ```

        Status: 200

        Response:

        ```
        {
            "bulkDownloadId": "7671653144481"
        }
        ```

    2. **Bad Request - Missing Required Parameter**

        Request Body: None

        Status: 400

        Response:

        ```
        {
            "detail": "Parameter \"videoIds\" is required"
        }
        ```

2. Get Download Result

    **URL**: {{base_url}}/bulk-download/

    **Method**: GET

    **Query Params**:
    | Parameter      | Type   | Required? |
    |----------------|--------|-----------|
    | bulkDownloadId | String | yes       |

    **Request Body**: None

    **Example Response**:

    1. **OK**

        URL: {{base_url}}/bulk-download/?bulkDownloadId=7671653144481

        Status: 200

        Response: zip file

    2. **Bad Request - Missing Required Parameter**

        URL: {{base_url}}/bulk-download/

        Status: 400

        Response:

        ```
        {
            "detail": "Parameter \"bulkDownloadId\" is required"
        }
        ```

    3. **Not Found - Data cannot be found or still in progress**

        URL: {{base_url}}/bulk-download/?bulkDownloadId=767165314448

        Status: 404

        Response:

        ```
        {
            "detail": "Data with id 767165314448 cannot be found or still in progress"
        }
        ```


## Websocket

1. Get Download Progress

    **URL**: ws://{{base_url}}/ws/bulk-download/{{bulk_download_id}}

    **Example Response**:

    ```
    {
      "message": 80
    }
    ````

    Notes:
    * 100 -> Finished
    * 80 -> 80% progress
    * -1 -> Failed
