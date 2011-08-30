<?php

/**
 * XMPP publish subscribe module
 * 
 * @package		PubSub
 * @author		Arjan Scherpenisse <arjan@mediamatic.nl>
 * @author		Robin Gareus <robin@mediamatic.nl>
 * @copyright	2008,2009 Mediamatic Lab
 * @version		$Id: PubSub.mod.php 50854 2010-11-15 21:36:58Z arjan $
 */

require_once ANYMETA_CORE . 'interfaces/Module.php';


class Devcamp10BanjoDinosaur extends Module
{

	/**
	 * Implementing iModule methods
	 *
	 */
	public function author()
	{
		return 'Arjan Scherpenisse';
	}

	public function description()
	{
		return 'Module for the Devcamp10banjodinosaur project';
	}

	public function version ()
	{
		return '1.0.0';
	}


    public function install()
    {
        require_once ANYMETA . 'Anymeta/Install/ACLInstaller.php';
        $inst = new Anymeta_ACLInstaller('Devcamp10 module');

        $inst->addSystemGroup('banjodinosaur', 'known users');
        $inst->addSystemUser('Banjo Dinosaur agent', 'arjan+banjodinosaur@mediamatic.nl', 'banjodinosaur', 'cyborg01');

        $inst->addACL('banjodinosaur', array('createkind', 'attachment', 'content', 'public'));
        $inst->addACL('banjodinosaur', array('edit', array('ownedit', 'ownpublish', 'owndelete'), 'content', array('system', 'public')));

		return true;
	}
}


/* vi:set ts=4 sts=4 sw=4 binary noeol: */

?>