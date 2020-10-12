#!groovy

properties(
    [disableConcurrentBuilds(),
    parameters(
        [string(defaultValue: '"restaurantes" AND "email" AND "Aranjuez"', description: 'The query you want to use to look for emails. Example: "restaurantes" AND "email" AND "Aranjuez"', name: 'QUERY', trim: false),
        choice(choices: ['Database', 'Xls file'], description: 'The formats to export the results of the query', name: 'EXPORT_TYPE'),
        string(defaultValue: 'emails_finder_results', description: 'The name of the files that will be exported', name: 'EXPORT_NAME', trim: false)]),
    [$class: 'GithubProjectProperty', displayName: '', projectUrlStr: 'https://github.com/alopezna5/google_emails_finder/']])

node{
    stage('Clone') {
        git branch: 'feat/jenkinsfile_added', url: 'https://github.com/alopezna5/google_emails_finder'
    }

    stage('Launch script') {
        sh """
            cd emails_finder
            python3 __main__.py -q \"${env.QUERY}\" -d  ${env.EXPORT_NAME}
        """
    }
}