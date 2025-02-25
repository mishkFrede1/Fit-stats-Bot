PGDMP                      }            accounts    16.3    16.3     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16404    accounts    DATABASE     |   CREATE DATABASE accounts WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE accounts;
                postgres    false            �            1259    24579    records    TABLE     q  CREATE TABLE public.records (
    user_id bigint NOT NULL,
    first_name text NOT NULL,
    username text,
    record_id integer NOT NULL,
    date date NOT NULL,
    training_type text,
    exercises text[],
    time_spent integer,
    state_of_health text,
    note text,
    burned_cal integer,
    gained_cal integer,
    measurements text[],
    sleep integer
);
    DROP TABLE public.records;
       public         heap    postgres    false            �            1259    24586    records_record_id_seq    SEQUENCE     �   CREATE SEQUENCE public.records_record_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.records_record_id_seq;
       public          postgres    false    218            �           0    0    records_record_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.records_record_id_seq OWNED BY public.records.record_id;
          public          postgres    false    219            �            1259    16415 	   schedules    TABLE       CREATE TABLE public.schedules (
    user_id bigint NOT NULL,
    first_name text NOT NULL,
    username text,
    days text[],
    training_time time without time zone,
    training_type text,
    training_id integer NOT NULL,
    exercises text[],
    training_name text
);
    DROP TABLE public.schedules;
       public         heap    postgres    false            �            1259    16438    schedules_training_id_seq    SEQUENCE     �   CREATE SEQUENCE public.schedules_training_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.schedules_training_id_seq;
       public          postgres    false    216            �           0    0    schedules_training_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.schedules_training_id_seq OWNED BY public.schedules.training_id;
          public          postgres    false    217            �            1259    16405    users    TABLE     ;  CREATE TABLE public.users (
    user_id bigint NOT NULL,
    registered_at date NOT NULL,
    first_name text NOT NULL,
    username text,
    gender_female boolean NOT NULL,
    age integer NOT NULL,
    height integer NOT NULL,
    weight integer NOT NULL,
    goal text NOT NULL,
    notifications_time integer DEFAULT 0,
    notifications boolean DEFAULT true,
    friends bigint[],
    friends_trainings_visible boolean DEFAULT true,
    friends_records_visible boolean DEFAULT true,
    friends_stats_visible boolean DEFAULT true,
    records_filter_data text[]
);
    DROP TABLE public.users;
       public         heap    postgres    false            )           2604    24587    records record_id    DEFAULT     v   ALTER TABLE ONLY public.records ALTER COLUMN record_id SET DEFAULT nextval('public.records_record_id_seq'::regclass);
 @   ALTER TABLE public.records ALTER COLUMN record_id DROP DEFAULT;
       public          postgres    false    219    218            (           2604    16439    schedules training_id    DEFAULT     ~   ALTER TABLE ONLY public.schedules ALTER COLUMN training_id SET DEFAULT nextval('public.schedules_training_id_seq'::regclass);
 D   ALTER TABLE public.schedules ALTER COLUMN training_id DROP DEFAULT;
       public          postgres    false    217    216            �          0    24579    records 
   TABLE DATA           �   COPY public.records (user_id, first_name, username, record_id, date, training_type, exercises, time_spent, state_of_health, note, burned_cal, gained_cal, measurements, sleep) FROM stdin;
    public          postgres    false    218          �          0    16415 	   schedules 
   TABLE DATA           �   COPY public.schedules (user_id, first_name, username, days, training_time, training_type, training_id, exercises, training_name) FROM stdin;
    public          postgres    false    216   �       �          0    16405    users 
   TABLE DATA             COPY public.users (user_id, registered_at, first_name, username, gender_female, age, height, weight, goal, notifications_time, notifications, friends, friends_trainings_visible, friends_records_visible, friends_stats_visible, records_filter_data) FROM stdin;
    public          postgres    false    215          �           0    0    records_record_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.records_record_id_seq', 804, true);
          public          postgres    false    219            �           0    0    schedules_training_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.schedules_training_id_seq', 118, true);
          public          postgres    false    217            +           2606    16446    schedules schedules_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_pkey PRIMARY KEY (training_id);
 B   ALTER TABLE ONLY public.schedules DROP CONSTRAINT schedules_pkey;
       public            postgres    false    216            �   u  x�Ŗ�N1���S�rDK���~������DE� �J	�h{@ph�=��*�T)|��@�W�ߨ�q��B�JM�����ol�x�p��̅����o�ڋ�k���j��l��Y.js�G��򿺹W�y����퉽r��۵���={f��޸=���ݮ�@ϥ�Ɠ�I�}��'PP�*w��~�vl�����zk�a��O'�����ǋ��G��e�~#5�lo��t��]{��k;��Ğ�TA�a��70�*nA�������n�	F�-&;��=Ҟ�����>8Ƕ\'�W�K+�[�g����*�3n��B���"�ˌ1�)�	�����h=Y�l���#W�l���=[��j�X�H��N��m�t���[�멤-�1�f VLnP�c`�����*�0+Xٿ�R��2PT����& ��0��+�,�hX ���8��oD3��c�<�]�I��yP�)u�O�c�Ԅ����U��4`�ۘ������T�i�8�	��+��U�KT�o�4�>��>'?���=��+��+n��4`��j6�5�f�PjG6;EREn� ��PP��A���'����JH�=J��>��.����_/P5q��?�V�$[0У4�(����	)�|0Dc��fXZ�~����x�M���?L ���S�}��4�2���n��g���sw�^x�_���{�Y��>��Իw���ǻ�O��^c�5��i�aI�XN�ř/��E��R���ݢ
�����t9拹O�/�-9ty�����6����X�-,�q�L�qR��_��P�U���ܚ�j�cr�SL�3�ti!UB	-|w���,PU����$'��sTa��1A�<�L�;�k|���W���G�z�t�lK      �   o  x��V[OA~^~ņ�&���;˯�Cy�/iĄK�!$����h[L|��&}�
���f�Q�s��b@�4�,;s�̙�|�2�@I?+G��8˅���jɩ������J�Z[�W�P��i�Q\,+4����ѠƂ��es��y���a�N��n�c�4͖���Û�}�v�v����êXu�6��i��d*�O1��B���I[_����d*��d��̱��z9��eȭag�$WPn@:����ɶi�N���c�ݝ�O���z�R	����I��d�2ą9Ż����z.���10�9Ge�x��=<M���h�0qg�ɹ<5�K��0�h�d#!��z�L��tt8��dys�cy���ԇ�=�]>�bצ�pfF��c��=X��7{Q>�]*s��x&8q����& �^�UhtGJp����/�P*)����~��<w����|1f�*����Q#�n9㶢�X�ԧ�|�/^��|I,���t�ӶKj��/I�\�s�Ne�#�O"��G��/�!��F��)8Q��R��@���xfD��=�/��A�+v^�L����œ&��Q���@t��/�PY?�A_m�G�����j���F�,������Q��{����(��R��|�]=}���ަT��@���'Ht��Ks�	�+v����������^VG䇇��|�#s,�젔��K6��W�.�nfx�:��W��J�8G�gv!{D��=6���ʰ?�+���}�
x���8���,��1�\�S�,R}X񳾾��a�3�=$.��^��"7�^p/h��	|�/�Y��$:�C�R�����q�y�M�cb&���+:�bZ〡�M,��H$�-B�      �   ]  x��RKN�0]ON���Ac;��
,*,�	(i��A�R+E�ʂ�e(��.�g�����4�"˚���y�Y[��P*(�/4|�?C4��nܤ'z��vAﴤOZ��^��-a
��2@DV.�-z!7VH-L�Ѓ���Q���|�k�2�$�piQ���_ژ�;�9���YV��"��'yP�d�T�m/�kA[�Bm���"��y���֠����nK�����G]�iI��.`���优%���`%УKy��vяmI��N�?�u�A+*����k^��b؁�uX�	-k{�X3$"��-Q4(�Y���)��be��ݫ\p�_%7�,��r�L�*/:�<�D��8     