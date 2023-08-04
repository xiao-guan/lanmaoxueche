pipeline {
    agent any

    stages {
        stage('拉取代码') {
            steps {
                // 单行注释
                // git branch: 'main', credentialsId: "${sshkey}", url: 'https://github.com/xiao-guan/lanmaoxueche'
                // echo "${sshkey}"
                sh 'printenv'
            }
        }
        stage('运行脚本') {
            steps {
                // sh 'python3 --version'
                // sh 'pwd'
                sh "python3 lanmao.py --id ${id}"
            }
        }
    }
    post {
      success {
              script {
                    EMAIL_CONTENT = ''
                        EMAIL_CONTENT += '<hr/>(自动化构建邮件，无需回复！)<br/><hr/>'
                    EMAIL_CONTENT += '项目名称：$PROJECT_NAME<br/><br/>'
                    EMAIL_CONTENT += '项目描述：$JOB_DESCRIPTION<br/><br/>'
                    EMAIL_CONTENT += '运行编号：$BUILD_NUMBER<br/><br/>'
                    EMAIL_CONTENT += '运行结果：$BUILD_STATUS<br/><br/>'
                    EMAIL_CONTENT += '触发原因：${CAUSE}<br/><br/>'
                    EMAIL_CONTENT += '构建日志地址：<a href="${BUILD_URL}console">${BUILD_URL}console</a><br/><br/>'
                    EMAIL_CONTENT += '构建地址：<a href="$BUILD_URL">$BUILD_URL</a><br/><br/>'
                    EMAIL_CONTENT += '详情：${JELLY_SCRIPT,template="html"}<br/>'
                    EMAIL_CONTENT += '<hr/>'
                  emailext(subject: '${PROJECT_NAME}构建成功！',to: '${qqmail}',body: EMAIL_CONTENT)
              }
          }
          failure {
              script {
                    EMAIL_CONTENT = ''
                  EMAIL_CONTENT += '<hr/>(自动化构建邮件，无需回复！)<br/><hr/>'
                    EMAIL_CONTENT += '项目名称：$PROJECT_NAME<br/><br/>'
                    EMAIL_CONTENT += '项目描述：$JOB_DESCRIPTION<br/><br/>'
                    EMAIL_CONTENT += '运行编号：$BUILD_NUMBER<br/><br/>'
                    EMAIL_CONTENT += '运行结果：$BUILD_STATUS<br/><br/>'
                    EMAIL_CONTENT += '触发原因：${CAUSE}<br/><br/>'
                    EMAIL_CONTENT += '构建日志地址：<a href="${BUILD_URL}console">${BUILD_URL}console</a><br/><br/>'
                    EMAIL_CONTENT += '构建地址：<a href="$BUILD_URL">$BUILD_URL</a><br/><br/>'
                    EMAIL_CONTENT += '详情：${JELLY_SCRIPT,template="html"}<br/>'
                    EMAIL_CONTENT += '<hr/>'

                  emailext(subject: '${PROJECT_NAME}构建失败！',to: '${qqmail}',body: EMAIL_CONTENT)
              }
          }

    }
}

