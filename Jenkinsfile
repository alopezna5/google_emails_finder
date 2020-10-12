#!groovy

properties(
    [disableConcurrentBuilds(),
    parameters(
        [string(defaultValue: '"restaurantes" AND "email" AND "Aranjuez"', description: 'The query you want to use to look for emails. Example: "restaurantes" AND "email" AND "Aranjuez"', name: 'Query', trim: false),
        choice(choices: ['Database', 'Xls file'], description: 'The formats to export the results of the query', name: 'Export type'),
        string(defaultValue: '', description: 'The name of the files that will be exported', name: 'Export name', trim: false)]),
    [$class: 'GithubProjectProperty', displayName: '', projectUrlStr: 'https://github.com/alopezna5/google_emails_finder/']])

node{
    stage('Clone') {
        git 'https://github.com/alopezna5/google_emails_finder'
    }

    stage('Launch script') {
        sh """
            cd emails_finder
            ls
        """
    }
}