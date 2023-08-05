# Robots.txt file for http://www.salesforce.com
# All robots will spider the domain
#
Sitemap: https://www.salesforce.com/sitemap.xml
Sitemap: https://www.salesforce.com/ap/sitemap.xml
Sitemap: https://www.salesforce.com/au/sitemap.xml
Sitemap: https://www.salesforce.com/br/sitemap.xml
Sitemap: https://www.salesforce.com/ca/sitemap.xml
Sitemap: https://www.salesforce.com/cn/sitemap.xml
Sitemap: https://www.salesforce.com/cn/sitemap_b.xml
Sitemap: https://www.salesforce.com/de/sitemap.xml
Sitemap: https://www.salesforce.com/dk/sitemap.xml
Sitemap: https://www.salesforce.com/es/sitemap.xml
Sitemap: https://www.salesforce.com/fi/sitemap.xml
Sitemap: https://www.salesforce.com/fr/sitemap.xml
Sitemap: https://www.salesforce.com/fr-ca/sitemap.xml
Sitemap: https://www.salesforce.com/in/sitemap.xml
Sitemap: https://www.salesforce.com/it/sitemap.xml
Sitemap: https://www.salesforce.com/jp/sitemap.xml
Sitemap: https://www.salesforce.com/kr/sitemap.xml
Sitemap: https://www.salesforce.com/mx/sitemap.xml
Sitemap: https://www.salesforce.com/nl/sitemap.xml
Sitemap: https://www.salesforce.com/no/sitemap.xml
Sitemap: https://www.salesforce.com/ru/sitemap.xml
Sitemap: https://www.salesforce.com/se/sitemap.xml
Sitemap: https://www.salesforce.com/th/sitemap.xml
Sitemap: https://www.salesforce.com/tw/sitemap.xml
Sitemap: https://www.salesforce.com/uk/sitemap.xml
Sitemap: https://www.salesforce.com/eu/sitemap.xml
Sitemap: https://www.salesforce.com/hk/sitemap.xml
Sitemap: https://www.salesforce.com/my/sitemap.xml

#
# Keep mis-configured Microsoft SharePoint servers from hammering us
# This is not MSN Search (msnbot), but privately owned SharePoint installations
#
User-agent: MS Search 4.0 Robot
Disallow: /
User-agent: Mozilla/4.0 (compatible; MSIE 4.01; Windows NT; MS Search 4.0 Robot)
Disallow: /
User-agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT; MS Search 4.0 Robot)
Disallow: /
User-agent: Mozilla/4.0 (compatible; MSIE 4.01; Windows NT; MS Search 5.0 Robot)
Disallow: /
User-agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT; MS Search 5.0 Robot)
Disallow: /
#
User-agent: *
Disallow: /products/home-perf/
# Disallow: /at/
# Disallow: /crm-success-summer/
# Disallow: /crm/
Disallow: /email-friend.jsp
Disallow: /form/conf/
Disallow: /blog/.html.
# Disallow: /ie/
# Disallow: /marketplace/
# Disallow: /myfuture/
# Disallow: /newevents/
Disallow: /opencms/
# Disallow: /orderentry/
# Disallow: /person/
Disallow: /promos/
Disallow: /styleguide/
# Disallow: /services/
# Disallow: /servlet/
# Disallow: /site/
# Disallow: /soap/
# Disallow: /trainingsupport/
Disallow: /landing/
Disallow: /modules/
Disallow: /assets/pdf/misc/WP_5Reasons_022409.pdf
# Disallow: /web-common/
# Disallow: /usertutorial/
Disallow: /eu/testfile.jsp
Disallow: /uk/promos/
Disallow: /eu/promos/
Disallow: /de/promos/
Disallow: /es/promos/
Disallow: /fr/promos/
Disallow: /it/promos/
Disallow: /jp/promos/
Disallow: na1.salesforce.com/help/doc/en/salesforce_pubs_style_guide.pdf
# Company pages duped across locales
Disallow: /us/developer/docs/ajaxpre
Disallow: /us/developer/docs/ajax80
Disallow: /us/developer/docs/ajax90
Disallow: /us/developer/docs/ajax1*
Disallow: /us/developer/docs/ajax2*
Disallow: /us/developer/docs/ajax3*
Disallow: /us/developer/docs/ajax4*
Disallow: /us/developer/docs/apexcodepre
Disallow: /us/developer/docs/apexcode1*
Disallow: /us/developer/docs/apexcode2*
Disallow: /us/developer/docs/apexcode3*
Disallow: /us/developer/docs/apexcode4*
Disallow: /us/developer/docs/api_asynchpre
Disallow: /us/developer/docs/api_asynch1*
Disallow: /us/developer/docs/api_asynch2*
Disallow: /us/developer/docs/api_asynch3*
Disallow: /us/developer/docs/api_asynch4*
Disallow: /us/developer/docs/api_consolepre
Disallow: /us/developer/docs/api_console2*
Disallow: /us/developer/docs/api_console3*
Disallow: /us/developer/docs/api_console4*
Disallow: /us/developer/docs/api_metapre
Disallow: /us/developer/docs/api_meta1*
Disallow: /us/developer/docs/api_meta2*
Disallow: /us/developer/docs/api_meta3*
Disallow: /us/developer/docs/api_meta4*
Disallow: /us/developer/docs/api_restpre
Disallow: /us/developer/docs/api_rest2*
Disallow: /us/developer/docs/api_rest3*
Disallow: /us/developer/docs/api_rest4*
Disallow: /us/developer/docs/api_streamingpre
Disallow: /us/developer/docs/api_streaming2*
Disallow: /us/developer/docs/api_streaming3*
Disallow: /us/developer/docs/api_streaming4*
Disallow: /us/developer/docs/apipre
Disallow: /us/developer/docs/api80
Disallow: /us/developer/docs/api90
Disallow: /us/developer/docs/api1*
Disallow: /us/developer/docs/api2*
Disallow: /us/developer/docs/api3*
Disallow: /us/developer/docs/api4*
Disallow: /us/developer/docs/chatterapipre
Disallow: /us/developer/docs/chatterapi2*
Disallow: /us/developer/docs/chatterapi3*
Disallow: /us/developer/docs/chatterapi4*
Disallow: /us/developer/docs/dbcom_apipre
Disallow: /us/developer/docs/dbcom_api2*
Disallow: /us/developer/docs/dbcom_api3*
Disallow: /us/developer/docs/dbcom_api4*
Disallow: /us/developer/docs/dbcom_objectspre
Disallow: /us/developer/docs/dbcom_objects2*
Disallow: /us/developer/docs/dbcom_objects3*
Disallow: /us/developer/docs/dbcom_objects4*
Disallow: /us/developer/docs/dbcom_soql_soslpre
Disallow: /us/developer/docs/dbcom_soql_sosl2*
Disallow: /us/developer/docs/dbcom_soql_sosl3*
Disallow: /us/developer/docs/dbcom_soql_sosl4*
Disallow: /us/developer/docs/daaspre
Disallow: /us/developer/docs/daas140
Disallow: /us/developer/docs/fundamentalspre
Disallow: /us/developer/docs/knowledge_devpre
Disallow: /us/developer/docs/object_referencepre
Disallow: /us/developer/docs/object_reference2*
Disallow: /us/developer/docs/object_reference3*
Disallow: /us/developer/docs/object_reference4*
Disallow: /us/developer/docs/officetoolkit30
Disallow: /us/developer/docs/pagespre
Disallow: /us/developer/docs/pages1*
Disallow: /us/developer/docs/pages2*
Disallow: /us/developer/docs/pages3*
Disallow: /us/developer/docs/pages4*
Disallow: /us/developer/docs/sforce20
Disallow: /us/developer/docs/sforce30
Disallow: /us/developer/docs/sforce40
Disallow: /us/developer/docs/sforce50
Disallow: /us/developer/docs/sforce60
Disallow: /us/developer/docs/sforce70

# AMER testing
Disallow: /campaign/smb-b/
Disallow: /campaign/smb-c/
Disallow: /campaign/smb-d/

#
# Disallow: /uk/foundation/
# Disallow: /eu/foundation/
# Disallow: /au/foundation/
#
# Disallow: /uk/services-training/customer-support/
# Disallow: /uk/services-training/professional-services/
# Disallow: /uk/services-training/index.jsp
# Disallow: /eu/services-training/customer-support/
# Disallow: /eu/services-training/professional-services/
# Disallow: /eu/services-training/index.jsp
# Disallow: /au/services-training/customer-support/
# Disallow: /au/services-training/professional-services/
# Disallow: /au/services-training/index.jsp
#
# Disallow: /uk/platform/
# Disallow: /eu/platform/
# Disallow: /au/platform/
#
Disallow: /clear_login_cookie.html
Disallow: /clear_cookie.jsp
Disallow: /eu/homepage-flash-testing.jsp
Disallow: /uk/homepage-flash-testing.jsp
Disallow: /de/homepage-flash-testing.jsp
Disallow: /es/homepage-flash-testing.jsp
Disallow: /fr/homepage-flash-testing.jsp
Disallow: /it/homepage-flash-testing.jsp
Disallow: /homepage-flash-testing.jsp
#
Disallow: /appexchange/addedit_app.jsp
Disallow: /appexchange/addedit_datasheet.jsp
Disallow: /appexchange/addedit_logo.jsp
Disallow: /appexchange/addedit_pub.jsp
Disallow: /appexchange/addedit_screenshot.jsp
Disallow: /appexchange/addedit_thumbnail.jsp
Disallow: /appexchange/authentication.jsp
Disallow: /appexchange/categorise_app.jsp
Disallow: /appexchange/my_applications.jsp
Disallow: /appexchange/sub_for_rev.jsp
Disallow: /appexchange/addedit_evalunpw.jsp
Disallow: /appexchange/getitnow.jsp
Disallow: /appexchange/addedit_review.jsp
Disallow: /appexchange/partner_contact.jsp
Disallow: /appexchange/tryit.jsp
Disallow: /appexchange/tell_friend.jsp
Disallow: /appexchange/www.
Disallow: /appexchange/demo.jsp
Disallow: /appexchange/demoit.jsp
Disallow: /appexchange/downloadit.jsp
Disallow: /appexchange/learnmore.jsp
Disallow: /appexchange/getitnow.jsp
Disallow: /customers-appexchange/

Disallow: /assets/pdf/misc/state-of-sales-report-salesforce.pdf


#
Disallow: /democenter/
Disallow: /democenter/
#Disallow: /uk/democenter/
#Disallow: /eu/democenter/
#Disallow: /ie/democenter/
#Disallow: /de/democenter/
#Disallow: /fr/democenter/
#Disallow: /it/democenter/
#Disallow: /es/democenter/
Disallow: /democenterapp/
#
Disallow: /demo/is/
#
#Disallow: /de/campaigns/refer-a-friend.jsp
#Disallow: /eu/campaigns/refer-a-friend.jsp
#Disallow: /fr/campaigns/refer-a-friend.jsp
#Disallow: /it/campaigns/refer-a-friend.jsp
#Disallow: /uk/campaigns/refer-a-friend.jsp

Disallow: /dreamforceeurope/tracks/si/
#
# Disallow: /uk/events/details/a1x300000004DrwAAE.jsp
# Disallow: /uk/events/details/cf12-london/conf/*
# Disallow: /uk/events/details/cf12-london/facebook-form-content.jsp
# Disallow: /uk/events/details/cf12-london/facebook-form.jsp
# Disallow: /uk/events/details/cf12-london/grid-form-content.jsp
#
Disallow: /search.jsp
#
Disallow: /company/force_com_sites_terms.jsp
Disallow: /jp/company/force_com_sites_terms.jsp
# Disallow: /fr/company/force_com_sites_terms.jsp
#
Disallow: /assets/pdf/company/private/
#
Disallow: /jp/assets/pdf/
#
# Blocked /in/ on request from ALoon
# RH (09/11/09) Unlbocked /in/ on request from ALoon
# Disallow: /in/
#
# The line below was requested by MVozzo to block Search Engines from indexing the Quick Site test site as we are running a parallel site test in Q1-FY12.
Disallow: /au/intl/      
#
Disallow: /qe/      
User-agent: AdsBot-Google
Allow: /
#
# Added by jrietveld for EMEA cleanup
User-agent: *
# Disallow: /de/iss/
# Disallow: /de/events/details/conf/
# Disallow: /de/_app/
# Disallow: /de/platform/tco/
# Disallow: /de/form/
Disallow: /de/assets/
# Disallow: /fr/form/
Disallow: /fr/assets/
# Disallow: /se/form/
Disallow: /se/assets/
# Disallow: /es/form/
Disallow: /es/assets/
# Disallow: /it/form/
Disallow: /it/assets/
# Disallow: /nl/form/
Disallow: /nl/assets/
# Disallow: /uk/form/
Disallow: /uk/assets/
# Disallow: /eu/form/
Disallow: /eu/assets/

# EMEA SEM folders added by Joe Reid
Disallow: /eu/campaign/sem/
Disallow: /uk/campaign/sem/
Disallow: /de/campaign/sem/
Disallow: /fr/campaign/sem/
Disallow: /nl/campaign/sem/


#Block customer story filter URLS globally until filter fix is implemented by dev. Approved by Alex, Joe, Richard. AMER + EMEA

# STARTS
# Temporary rules to mitigate problems with faceted search in CSC.
# Block crawl of ._filter.alphaSort which is duplicate of /customer-success-stories/
# Note the $ delimiter so that this doesnt impact other URLs based on this stem:
Disallow: */customer-success-stories._filter.alphaSort$
Disallow: */customer-success-stories/._filter.alphaSort$

# Block all access to URLs using popularSort:
# Disallow: /es/customer-success-stories._filter.popularSort
# Disallow: /de/customer-success-stories._filter.popularSort
# Disallow: /fr/customer-success-stories._filter.popularSort
# Disallow: /it/customer-success-stories._filter.popularSort
# Disallow: /nl/customer-success-stories._filter.popularSort
# Disallow: /se/customer-success-stories._filter.popularSort
# Disallow: /uk/customer-success-stories._filter.popularSort
# Disallow: /eu/customer-success-stories._filter.popularSort
# Uncomment next line to apply to all locales
Disallow: */customer-success-stories._filter.popularSort
Disallow: */customer-success-stories/._filter.popularSort

# Block all access to URLs using newestSort:
# Disallow: /es/customer-success-stories._filter.newestSort
# Disallow: /de/customer-success-stories._filter.newestSort
# Disallow: /fr/customer-success-stories._filter.newestSort
# Disallow: /it/customer-success-stories._filter.newestSort
# Disallow: /nl/customer-success-stories._filter.newestSort
# Disallow: /se/customer-success-stories._filter.newestSort
# Disallow: /uk/customer-success-stories._filter.newestSort
# Disallow: /eu/customer-success-stories._filter.newestSort
# Uncomment next line to apply to all locales
Disallow: */customer-success-stories._filter.newestSort
Disallow: */customer-success-stories/._filter.newestSort

# Block crawl where 2 or more categories are used with services filter. The final . surrounded by * should match any multi-category filter URL:
# Disallow: /es/customer-success-stories._filter.alphaSort.S*.*
# Disallow: /de/customer-success-stories._filter.alphaSort.S*.*
# Disallow: /fr/customer-success-stories._filter.alphaSort.S*.*
# Disallow: /it/customer-success-stories._filter.alphaSort.S*.*
# Disallow: /nl/customer-success-stories._filter.alphaSort.S*.*
# Disallow: /se/customer-success-stories._filter.alphaSort.S*.*
# Disallow: /uk/customer-success-stories._filter.alphaSort.S*.*
# Disallow: /eu/customer-success-stories._filter.alphaSort.S*.*
# Uncomment next line to apply to all locales
Disallow: */customer-success-stories._filter.alphaSort.S*.*
Disallow: */customer-success-stories/._filter.alphaSort.S*.*


#added new Deny rules to block bots to crawl missed filter URLs.
User-agent: *
Disallow: */customer-success-stories/*.*._filter
Disallow: */customer-success-stories.*._filter
Disallow: */customer-success-stories.[a-z]*Sort.*
Disallow: */customer-success-stories._filter.[a-z]*Sort.*

# Block crawl where 2 or more categories are used with products filter. The final . surrounded by * should match any multi-category filter URL:
# Disallow: /es/customer-success-stories._filter.alphaSort.P*.*
# Disallow: /de/customer-success-stories._filter.alphaSort.P*.*
# Disallow: /fr/customer-success-stories._filter.alphaSort.P*.*
# Disallow: /it/customer-success-stories._filter.alphaSort.P*.*
# Disallow: /nl/customer-success-stories._filter.alphaSort.P*.*
# Disallow: /se/customer-success-stories._filter.alphaSort.P*.*
# Disallow: /uk/customer-success-stories._filter.alphaSort.P*.*
# Disallow: /eu/customer-success-stories._filter.alphaSort.P*.*
# Uncomment next line to apply to all locales
Disallow: */customer-success-stories._filter.alphaSort.P*.*
Disallow: */customer-success-stories/._filter.alphaSort.P*.*

# Block crawl where 2 or more categories are used with industries filter. The final . surrounded by * should match any multi-category filter URL:
# Disallow: /es/customer-success-stories._filter.alphaSort.I*.*
# Disallow: /de/customer-success-stories._filter.alphaSort.I*.*
# Disallow: /fr/customer-success-stories._filter.alphaSort.I*.*
# Disallow: /it/customer-success-stories._filter.alphaSort.I*.*
# Disallow: /nl/customer-success-stories._filter.alphaSort.I*.*
# Disallow: /se/customer-success-stories._filter.alphaSort.I*.*
# Disallow: /uk/customer-success-stories._filter.alphaSort.I*.*
# Disallow: /eu/customer-success-stories._filter.alphaSort.I*.*
# Uncomment next line to apply to all locales
Disallow: */customer-success-stories._filter.alphaSort.I*.*
Disallow: */customer-success-stories/._filter.alphaSort.I*.*

# Block crawl where 2 or more categories are used with business size filter. The final . surrounded by * should match any multi-category filter URL:
# Disallow: /es/customer-success-stories._filter.alphaSort.BS*.*
# Disallow: /de/customer-success-stories._filter.alphaSort.BS*.*
# Disallow: /fr/customer-success-stories._filter.alphaSort.BS*.*
# Disallow: /it/customer-success-stories._filter.alphaSort.BS*.*
# Disallow: /nl/customer-success-stories._filter.alphaSort.BS*.*
# Disallow: /se/customer-success-stories._filter.alphaSort.BS*.*
# Disallow: /uk/customer-success-stories._filter.alphaSort.BS*.*
# Disallow: /eu/customer-success-stories._filter.alphaSort.BS*.*
# Uncomment next line to apply to all locales
Disallow: */customer-success-stories._filter.alphaSort.BS*.*
Disallow: */customer-success-stories/._filter.alphaSort.BS*.*

# Block crawl where 2 or more categories are used with business type filter. The final . surrounded by * should match any multi-category filter URL:
# Disallow: /es/customer-success-stories._filter.alphaSort.BT*.*
# Disallow: /de/customer-success-stories._filter.alphaSort.BT*.*
# Disallow: /fr/customer-success-stories._filter.alphaSort.BT*.*
# Disallow: /it/customer-success-stories._filter.alphaSort.BT*.*
# Disallow: /nl/customer-success-stories._filter.alphaSort.BT*.*
# Disallow: /se/customer-success-stories._filter.alphaSort.BT*.*
# Disallow: /uk/customer-success-stories._filter.alphaSort.BT*.*
# Disallow: /eu/customer-success-stories._filter.alphaSort.BT*.*
# Uncomment next line to apply to all locales
Disallow: */customer-success-stories._filter.alphaSort.BT*.* 
Disallow: */customer-success-stories/._filter.alphaSort.BT*.* 
# ENDS

# Rules will block when 2 or more facets are activated, but allow single facets to be crawled:
Disallow: *services/success-plans/accelerators._filter.S*.*
Disallow: */services/success-plans/accelerators._filter.RG*.*
Disallow: */services/success-plans/accelerators._filter.P*.*
Disallow: *services/success-plans/accelerators/._filter.S*.*
Disallow: */services/success-plans/accelerators/._filter.RG*.*
Disallow: */services/success-plans/accelerators/._filter.P*.*
#
# First 2 rules blocks the duplicate index, $ delimiter avoids picking up valid pagination URLs:
Disallow: */services/learn/classes/._filter.alphaSort/$
Disallow: */services/learn/classes._filter.alphaSort/$
# Next rules will fire when more than one facet is activated, or when a subpage of facet is requested, but allow individual facets to be crawled:
Disallow: */services/learn/classes._filter.alphaSort.re*.*
Disallow: */services/learn/classes._filter.alphaSort.P*.*/
Disallow: */services/learn/classes/._filter.alphaSort.re*.*
Disallow: */services/learn/classes/._filter.alphaSort.P*.*/

#
# Blocking Acunetix
# 
#

User-agent: Acunetix Web Vulnerability Scanner
Disallow: /

User-agent: Acunetix Security Scanner
Disallow: /

Disallow: /products/commerce-cloud/partner-marketplace/.
Disallow: /products/einstein/ai-research.
Disallow: /blog/.
Disallow: /search/.

Disallow: /*.pdf$
Disallow: /conf/ 
Disallow: /search/
Disallow: /content/dam/
Disallow: /*._filter.
Disallow: /login-messages/
Disallow: /is/
Disallow: /form/pdf/*

