# scraping-test

## 実行方法

    docker-compose build && docker-compose up

## CRONへの登録
3分おきに実行の例

    0-59/3 * * * *  cd /home/admin/scraping-test && /usr/bin/docker-compose up
