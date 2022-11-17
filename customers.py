from dotenv import load_dotenv
import os


load_dotenv()

test_list_trakt = []
test_list_av = []
test_list_petr = []
test_list_m2o = []
test_list_axis = []
test_list_avtorum = []
test_list_july = []
test_list_chl = []
test_list_mias = []
test_list_skoda_planeta = []
test_list_geely_planeta = []
test_list_used_planeta = []
test_list_partner_auto = []
test_list_avtograd = []
test_list_chery_planeta = []
test_list_forwardsurgut = []
test_list_forwardtyumen = []
test_list_kiaring = []
test_list_UTC_lada_new = []
test_list_UTC_lada_used = []
test_list_UTC_mazda_new = []
test_list_UTC_mazda_used = []
test_list_avtopark_yvl = []
test_list_forward_auto = []
test_list_avtoset_rf = []
test_list_USED_Surgut = []
test_list_alfa_garant = []
test_list_west_wind = []
test_list_VM_Novosib = []
test_list_Gepard = []
test_list_AvtomirNSK = []
test_list_Avtoplus_EKT = []

signal_for_clean = []


def make_message(name_group, name, send_data) -> list:
    text = f'{name} - {send_data[0]}/{send_data[1]}'
    if name_group == 'Avangard':
        test_list_av.append(text)
        return test_list_av
    elif name_group == 'avtotrakt':
        test_list_trakt.append(text)
        return test_list_trakt
    elif name_group == 'Petrovsky':
        test_list_petr.append(text)
        return test_list_petr
    elif name_group == 'M2O':
        test_list_m2o.append(text)
        return test_list_m2o
    elif name_group == 'axis':
        test_list_axis.append(text)
        return test_list_axis
    elif name_group == 'avtorum':
        test_list_avtorum.append(text)
        return test_list_avtorum
    elif name_group == 'reginas_autoru':
        test_list_chl.append(text)
        return test_list_chl
    elif name_group == 'july':
        test_list_july.append(text)
        return test_list_july
    elif name_group == 'mias':
        test_list_mias.append(text)
        return test_list_mias
    elif name_group == 'skoda_planeta':
        test_list_skoda_planeta.append(text)
        return test_list_skoda_planeta
    elif name_group == 'geely_planeta':
        test_list_geely_planeta.append(text)
        return test_list_geely_planeta
    elif name_group == 'used_planeta':
        test_list_used_planeta.append(text)
        return test_list_used_planeta
    elif name_group == 'autopartner':
        test_list_partner_auto.append(text)
        return test_list_partner_auto
    elif name_group == 'avtograd':
        test_list_avtograd.append(text)
        return test_list_avtograd
    elif name_group == 'chery_planeta':
        test_list_chery_planeta.append(text)
        return test_list_chery_planeta
    elif name_group == 'forwardsurgut':
        test_list_forwardsurgut.append(text)
        return test_list_forwardsurgut
    elif name_group == 'forward_tyumen':
        test_list_forwardtyumen.append(text)
        return test_list_forwardtyumen
    elif name_group == 'ring':
        test_list_kiaring.append(text)
        return test_list_kiaring
    elif name_group == 'UTC_lada_new':
        test_list_UTC_lada_new.append(text)
        return test_list_UTC_lada_new
    elif name_group == 'UTC_lada_used':
        test_list_UTC_lada_used.append(text)
        return test_list_UTC_lada_used
    elif name_group == 'UTC_mazda_used':
        test_list_UTC_mazda_used.append(text)
        return test_list_UTC_mazda_used
    elif name_group == 'UTC_mazda_new':
        test_list_UTC_mazda_new.append(text)
        return test_list_UTC_mazda_new
    elif name_group == 'Avtopark':
        test_list_avtopark_yvl.append(text)
        return test_list_avtopark_yvl
    elif name_group == 'Forward_auto':
        test_list_forward_auto.append(text)
        return test_list_forward_auto
    elif name_group == 'Avtoset_RF':
        test_list_avtoset_rf.append(text)
        return test_list_avtoset_rf
    elif name_group == 'USED_Surgut':
        test_list_USED_Surgut.append(text)
        return test_list_USED_Surgut
    elif name_group == 'Alfa_garant':
        test_list_alfa_garant.append(text)
        return test_list_alfa_garant
    elif name_group == 'West_wind':
        test_list_west_wind.append(text)
        return test_list_west_wind
    elif name_group == 'VM_Novosib':
        test_list_VM_Novosib.append(text)
        return test_list_VM_Novosib
    elif name_group == 'Gepard':
        test_list_Gepard.append(text)
        return test_list_Gepard
    elif name_group == 'AvtomirNSK':
        test_list_AvtomirNSK.append(text)
        return test_list_AvtomirNSK
    elif name_group == 'Avtoplus_EKT':
        test_list_Avtoplus_EKT.append(text)
        return test_list_Avtoplus_EKT
