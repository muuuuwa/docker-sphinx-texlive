=====================
docker-sphinx-texlive
=====================

Docker image for Sphinx PDF build.

build::

   $ docker build --rm -t tokibito/sphinx-texlive .

run::

   $ docker run --rm -v /path/to/directory/:/docs/ tokibito/sphinx-texlive:latest


実行の流れ
==================
gitbucket -> lamda -> ECS -> ECRからイメージをダウンロード -> 実行

* Dockerfile
    * Dockerfile本体
* makezipfile.sh*
    * lambdaを作るファイル
* requirements.txt
    * Dockerfile で追加するためのもの
* run_ecs_task.py
    * lambda function 本体
* test_docker-run.sh*
    * 環境変数を設定してDocker run するスクリプト。このDockerImageはECRにupされ、ECSで実行される
* test_lambdafunc.sh*
    * lambda function のダミー実行を行うスクリプト。ECS経由で実行させる
* test_upload_pdf.sh*
    * PDFをUPするスクリプトのテスト
* tmp_check-push-event.py
    * GitBucket からのWeb通知をハンドリングするための検証スクリプト
* upload_pdf.py
    * PDFをUPするスクリプト。DockerImage に追加される。
