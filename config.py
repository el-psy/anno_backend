import os

config = {
	'cors':{ # 同源配置
		'resoueces': {

		},
		'origins':[
			'http://localhost:5173' # 前端的位置
		],
		'methods':[
			"GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE" # 允许访问的方式
		],
		'expose_headers':None,
		'allow_headers':'*',
		'supports_credentials':False,
		'max_age':None,
		'send_wildcard':False,
		'vary_header':True
	},
	'flask':{ # 还没放到代码中。。
		'SECRET_KEY':'dev' # flask的加密密码，如果需要将用户密码加密的话需要生成一个
	},
	'database':{ # 数据库配置
		'path': os.path.join(os.getcwd(), 'database', 'db.sqlite'),
		'dir': os.path.join(os.getcwd(), 'database'),
		'init_script':'schema.sql'
	},
	'auth':{ # JWT 配置
		'default_token_keep_time':864000, # json web token 生效时长，秒
		'default_secret_length':32, # 密码长度
	}
}