create table semana_cardapio(
	id_semana int primary key auto_increment,
	data_inicio datetime not null, 
	data_fim datetime not null
);

create table dia_cardapio(
	id_dia int primary key auto_increment,
	id_semana int,
	data_dia datetime not null,
	nome_dia datetime not null
);

create table refeicao(
	id_refeicao int primary key auto_increment,
    nome_refeicao varchar(50) not null 
);

create table categoria_item(
	id_categoria int primary key auto_increment,
	nome_categoria varchar(50) not null
);

create table item_cardapio(
	id_item int primary key auto_increment,
	nome_item varchar(50) not null,
	descricao varchar(255) not null
);

create table cardapio(
id_cardapio int primary key auto_increment,
id_dia int ,
id_refeicao int,
id_categoria int,
id_item int
);


-- foreign keys do banco de dados
alter table dia_cardapio
	add constraint fk_id_semana
		foreign key (id_semana) references semana_cardapio(id_semana);
        
alter table cardapio
	add constraint fk_id_dia
		foreign key (id_dia) references dia_cardapio(id_dia),
	
    add constraint fk_id_refeicao
		foreign key (id_refeicao) references refeicao(id_refeicao),
	
    add constraint fk_id_categoria
		foreign key (id_categoria) references categoria_item(id_categoria),
	
    add constraint fk_id_item
		foreign key (id_item) references item_cardapio(id_item);

ALTER TABLE dia_cardapio
MODIFY COLUMN nome_dia VARCHAR(20) NOT NULL;
	
