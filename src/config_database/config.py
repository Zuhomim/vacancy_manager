from configparser import ConfigParser


def config(filename='./config_database/database.ini', section='postgresql'):

    config_ = ConfigParser()
    config_.read(filename)
    db = {}
    if config_.has_section(section):
        params = config_.items(section)
        for param in params:
            db[param[0]] = param[1]

    else:
        raise Exception("Параметр {0} не найден в {1} file.".format(section, filename))

    return db
